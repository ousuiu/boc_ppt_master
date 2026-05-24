#!/usr/bin/env python3
"""Shared SVG helpers for the local BOC PPT builder skill."""

from __future__ import annotations

import os
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath


HREF_RE = re.compile(
    r'(?P<attr>\b(?:xlink:href|href)\s*=\s*)(?P<quote>["\'])(?P<value>.*?)(?P=quote)',
    re.IGNORECASE,
)
PAGE_PAIR_RE = re.compile(r"\{\{PAGE_NUM\}\}\s*/\s*\{\{TOTAL_PAGES\}\}")
PAGE_TEXT_RE = re.compile(
    r"(?P<open><text\b"
    r"(?=[^>]*(?:\by\s*=\s*['\"](?:68\d|69\d|700)['\"]|\bid\s*=\s*['\"][^'\"]*page[^'\"]*['\"]))"
    r"[^>]*>\s*)"
    r"(?P<value>\d{1,4}\s*/\s*\d{1,4})"
    r"(?P<close>\s*</text>)",
    re.IGNORECASE | re.DOTALL,
)
SVG_CLOSE_RE = re.compile(r"\s*</svg>\s*$", re.IGNORECASE)


@dataclass
class AssetRewriteResult:
    text: str
    refs: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    rewritten_count: int = 0


def is_local_asset_ref(value: str) -> bool:
    ref = value.strip()
    lowered = ref.lower()
    if not ref:
        return False
    if ref.startswith("#"):
        return False
    return not (
        lowered.startswith("data:")
        or lowered.startswith("http://")
        or lowered.startswith("https://")
        or lowered.startswith("mailto:")
        or lowered.startswith("javascript:")
    )


def ref_basename(value: str) -> str:
    clean = value.replace("\\", "/").split("#", 1)[0].split("?", 1)[0]
    return PurePosixPath(clean).name


def local_asset_refs(svg_text: str) -> list[str]:
    refs: list[str] = []
    for match in HREF_RE.finditer(svg_text):
        value = match.group("value")
        if is_local_asset_ref(value):
            refs.append(value)
    return refs


def build_asset_index(asset_dir: Path) -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = {}
    if not asset_dir.exists():
        return index
    for path in asset_dir.rglob("*"):
        if path.is_file():
            index.setdefault(path.name.lower(), []).append(path)
    return index


def build_asset_index_from_dirs(asset_dirs: list[Path]) -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = {}
    for asset_dir in asset_dirs:
        if not asset_dir.exists():
            continue
        for path in asset_dir.rglob("*"):
            if path.is_file():
                index.setdefault(path.name.lower(), []).append(path)
    return index


def resolve_asset(ref: str, asset_index: dict[str, list[Path]]) -> Path | None:
    name = ref_basename(ref)
    if not name:
        return None
    matches = asset_index.get(name.lower(), [])
    if not matches:
        return None
    return sorted(matches, key=lambda item: len(str(item)))[0]


def relative_href(svg_path: Path, asset_path: Path) -> str:
    rel = os.path.relpath(asset_path.resolve(), svg_path.parent.resolve())
    return rel.replace(os.sep, "/")


def rewrite_asset_refs_in_text(
    svg_text: str,
    svg_path: Path,
    asset_index: dict[str, list[Path]],
) -> AssetRewriteResult:
    refs: list[str] = []
    missing: list[str] = []
    rewritten_count = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal rewritten_count
        value = match.group("value")
        if not is_local_asset_ref(value):
            return match.group(0)

        refs.append(value)
        asset_path = resolve_asset(value, asset_index)
        if asset_path is None:
            missing.append(value)
            return match.group(0)

        new_value = relative_href(svg_path, asset_path)
        if new_value != value:
            rewritten_count += 1
        return f"{match.group('attr')}{match.group('quote')}{new_value}{match.group('quote')}"

    text = HREF_RE.sub(replace, svg_text)
    return AssetRewriteResult(
        text=text,
        refs=refs,
        missing=sorted(set(missing)),
        rewritten_count=rewritten_count,
    )


def seed_asset_dir_from_refs(
    svg_paths: list[Path],
    asset_dir: Path,
    fallback_asset_dirs: list[Path],
) -> tuple[int, list[str]]:
    """Copy referenced assets from known template asset directories when missing."""
    fallback_index = build_asset_index_from_dirs(fallback_asset_dirs)
    if not fallback_index:
        return 0, []

    asset_index = build_asset_index(asset_dir)
    refs: list[str] = []
    for svg_path in svg_paths:
        if not svg_path.exists():
            continue
        try:
            text = svg_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = svg_path.read_text(encoding="utf-8-sig")
        refs.extend(local_asset_refs(text))

    copied_count = 0
    unresolved: list[str] = []
    for ref in sorted(set(refs), key=str.lower):
        name = ref_basename(ref)
        if not name or name.lower() in asset_index:
            continue

        fallback_path = resolve_asset(ref, fallback_index)
        if fallback_path is None:
            unresolved.append(ref)
            continue

        asset_dir.mkdir(parents=True, exist_ok=True)
        target = asset_dir / fallback_path.name
        if not target.exists():
            shutil.copy2(fallback_path, target)
            copied_count += 1
        asset_index.setdefault(target.name.lower(), []).append(target)

    return copied_count, sorted(set(unresolved))


def extract_page_pairs(svg_text: str) -> list[tuple[int, int]]:
    pairs: list[tuple[int, int]] = []
    for match in PAGE_TEXT_RE.finditer(svg_text):
        page, total = re.match(r"(\d{1,4})\s*/\s*(\d{1,4})", match.group("value")).groups()
        pairs.append((int(page), int(total)))
    return pairs


def replace_page_number(
    svg_text: str,
    page_num: int,
    total_pages: int,
    add_if_missing: bool = True,
) -> tuple[str, int]:
    replacement = f"{page_num} / {total_pages}"
    text, pair_count = PAGE_PAIR_RE.subn(replacement, svg_text)

    individual_count = text.count("{{PAGE_NUM}}") + text.count("{{TOTAL_PAGES}}")
    if individual_count:
        text = text.replace("{{PAGE_NUM}}", str(page_num)).replace("{{TOTAL_PAGES}}", str(total_pages))

    def replace_text(match: re.Match[str]) -> str:
        return f"{match.group('open')}{replacement}{match.group('close')}"

    text, text_count = PAGE_TEXT_RE.subn(replace_text, text)
    total_count = pair_count + individual_count + text_count

    if total_count == 0 and add_if_missing:
        injected = (
            '\n    <!-- Page number inserted by boc-ppt-builder -->\n'
            f'    <text id="boc-page-number" x="640" y="690" text-anchor="middle" '
            f'font-family="SimHei, PingFang SC, Arial, sans-serif" font-size="14" '
            f'fill="#8A9099">{replacement}</text>\n'
        )
        if SVG_CLOSE_RE.search(text):
            text = SVG_CLOSE_RE.sub(injected + "</svg>\n", text)
        else:
            text = text.rstrip() + injected
        total_count = 1

    return text, total_count
