#!/usr/bin/env python3
"""Validate BOC PPT chapter folders and local SVG asset references."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

from common_svg import (
    build_asset_index,
    local_asset_refs,
    rewrite_asset_refs_in_text,
    seed_asset_dir_from_refs,
)


CHAPTER_DIR_RE = re.compile(r"^c(\d+)-(.+)$", re.IGNORECASE)
PAGE_FILE_RE = re.compile(r"^page(\d+)\.svg$", re.IGNORECASE)
TOP_LEVEL_PAGE_RE = re.compile(r"^(cover|toc|ending|chapter\d+)\.svg$", re.IGNORECASE)
IGNORED_DIRS = {"asset", "assets", "final_svg", "output_svg", "output_pptx", "backup", "exports"}


@dataclass(frozen=True)
class ChapterInfo:
    number: int
    title: str
    path: Path
    pages: list[Path]


@dataclass
class ValidationResult:
    chapters: list[ChapterInfo]
    errors: list[str]
    warnings: list[str]
    rewritten_count: int = 0
    copied_asset_count: int = 0

    @property
    def ok(self) -> bool:
        return not self.errors


def discover_chapters(chapters_dir: Path) -> tuple[list[ChapterInfo], list[str]]:
    errors: list[str] = []
    chapters: list[ChapterInfo] = []

    if not chapters_dir.exists():
        return [], [f"Missing directory: {chapters_dir}"]
    if not chapters_dir.is_dir():
        return [], [f"Not a directory: {chapters_dir}"]

    candidate_dirs = [item for item in chapters_dir.iterdir() if item.is_dir() and item.name not in IGNORED_DIRS]
    for chapter_dir in sorted(candidate_dirs, key=lambda item: item.name.lower()):
        match = CHAPTER_DIR_RE.match(chapter_dir.name)
        if not match:
            errors.append(
                f"Invalid chapter directory name: {chapter_dir.name}. Expected c[章节序号]-[章节标题]."
            )
            continue

        number = int(match.group(1))
        title = match.group(2).strip()
        svg_files = sorted(chapter_dir.glob("*.svg"), key=lambda item: item.name.lower())
        invalid_files = [path.name for path in svg_files if not PAGE_FILE_RE.match(path.name)]
        if invalid_files:
            errors.append(
                f"{chapter_dir.name} contains SVG files not named page[章节内页码序号].svg: "
                + ", ".join(invalid_files)
            )

        pages = [path for path in svg_files if PAGE_FILE_RE.match(path.name)]
        if not pages:
            errors.append(f"{chapter_dir.name} contains no page[章节内页码序号].svg files.")
        else:
            page_numbers = sorted(int(PAGE_FILE_RE.match(path.name).group(1)) for path in pages if PAGE_FILE_RE.match(path.name))
            expected = list(range(1, len(page_numbers) + 1))
            if page_numbers != expected:
                errors.append(
                    f"{chapter_dir.name} page numbering is not continuous from 1: "
                    f"found {page_numbers}, expected {expected}."
                )

        chapters.append(ChapterInfo(number=number, title=title, path=chapter_dir, pages=pages))

    if not chapters:
        errors.append("No chapter folders found. Expected folders like c1-章节标题.")
        return [], errors

    chapter_numbers = sorted(chapter.number for chapter in chapters)
    expected_numbers = list(range(1, len(chapter_numbers) + 1))
    if chapter_numbers != expected_numbers:
        errors.append(
            f"Chapter numbering is not continuous from 1: found {chapter_numbers}, expected {expected_numbers}."
        )

    duplicates = sorted({number for number in chapter_numbers if chapter_numbers.count(number) > 1})
    if duplicates:
        errors.append(f"Duplicate chapter numbers found: {duplicates}.")

    return sorted(chapters, key=lambda chapter: chapter.number), errors


def collect_top_level_svgs(chapters_dir: Path) -> list[Path]:
    if not chapters_dir.exists():
        return []
    return sorted(
        [path for path in chapters_dir.glob("*.svg") if TOP_LEVEL_PAGE_RE.match(path.name)],
        key=lambda item: item.name.lower(),
    )


def validate_asset_refs(svg_paths: list[Path], asset_dir: Path, fix_assets: bool) -> tuple[list[str], list[str], int]:
    errors: list[str] = []
    warnings: list[str] = []
    rewritten_count = 0
    asset_index = build_asset_index(asset_dir)

    for svg_path in svg_paths:
        try:
            text = svg_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = svg_path.read_text(encoding="utf-8-sig")

        refs = local_asset_refs(text)
        if refs and not asset_dir.exists():
            errors.append(f"{svg_path} references local assets, but asset directory is missing: {asset_dir}")
            continue
        if not refs:
            continue

        result = rewrite_asset_refs_in_text(text, svg_path, asset_index)
        if result.missing:
            errors.append(
                f"{svg_path} has asset references missing from {asset_dir}: "
                + ", ".join(result.missing)
            )
        elif fix_assets and result.rewritten_count:
            svg_path.write_text(result.text, encoding="utf-8")
            rewritten_count += result.rewritten_count

    if asset_dir.exists() and not any(local_asset_refs(path.read_text(encoding="utf-8", errors="ignore")) for path in svg_paths):
        warnings.append("No local SVG asset references were found.")

    return errors, warnings, rewritten_count


def validate_chapters(
    chapters_dir: Path,
    fix_assets: bool = False,
    include_top_level: bool = False,
    template_asset_dirs: list[Path] | None = None,
) -> ValidationResult:
    chapters, errors = discover_chapters(chapters_dir)
    warnings: list[str] = []

    svg_paths: list[Path] = []
    for chapter in chapters:
        svg_paths.extend(chapter.pages)
    if include_top_level:
        svg_paths.extend(collect_top_level_svgs(chapters_dir))

    copied_asset_count = 0
    if fix_assets and svg_paths and template_asset_dirs:
        copied_asset_count, _ = seed_asset_dir_from_refs(
            svg_paths=svg_paths,
            asset_dir=chapters_dir / "asset",
            fallback_asset_dirs=template_asset_dirs,
        )
        if copied_asset_count:
            warnings.append(
                f"Copied {copied_asset_count} referenced template asset(s) into {chapters_dir / 'asset'}."
            )

    asset_errors, asset_warnings, rewritten_count = validate_asset_refs(
        svg_paths=svg_paths,
        asset_dir=chapters_dir / "asset",
        fix_assets=fix_assets,
    )
    errors.extend(asset_errors)
    warnings.extend(asset_warnings)

    return ValidationResult(
        chapters=chapters,
        errors=errors,
        warnings=warnings,
        rewritten_count=rewritten_count,
        copied_asset_count=copied_asset_count,
    )


def default_boc_template_assets_dir(project_root: Path) -> Path:
    return (
        project_root
        / "ppt-master"
        / "skills"
        / "ppt-master"
        / "templates"
        / "decks"
        / "中国银行"
        / "assets"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate ppt_chapters structure and SVG assets.")
    parser.add_argument("--project-root", default=str(Path.cwd()), help="Project root, default: current directory.")
    parser.add_argument("--chapters-dir", default=None, help="Explicit ppt_chapters path.")
    parser.add_argument("--fix-assets", action="store_true", help="Rewrite SVG asset references to the correct relative path.")
    parser.add_argument(
        "--include-top-level",
        action="store_true",
        help="Also validate cover.svg, toc.svg, ending.svg, and chapterN.svg asset refs.",
    )
    parser.add_argument(
        "--template-assets-dir",
        default=None,
        help="Fallback asset directory used with --fix-assets. Defaults to ppt-master's 中国银行 deck assets.",
    )
    parser.add_argument(
        "--no-template-assets",
        action="store_true",
        help="Do not copy missing assets from the bundled 中国银行 deck template.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    chapters_dir = Path(args.chapters_dir).resolve() if args.chapters_dir else project_root / "ppt_chapters"
    template_asset_dirs: list[Path] = []
    if args.fix_assets and not args.no_template_assets:
        template_asset_dirs.append(
            Path(args.template_assets_dir).resolve()
            if args.template_assets_dir
            else default_boc_template_assets_dir(project_root)
        )

    result = validate_chapters(
        chapters_dir=chapters_dir,
        fix_assets=args.fix_assets,
        include_top_level=args.include_top_level,
        template_asset_dirs=template_asset_dirs,
    )

    if result.errors:
        print("[ERROR] ppt_chapters validation failed:")
        for error in result.errors:
            print(f"  - {error}")
    else:
        print("[OK] ppt_chapters structure and asset references passed.")
        print(f"  Chapters: {len(result.chapters)}")
        print(f"  Template assets copied: {result.copied_asset_count}")
        print(f"  Asset references rewritten: {result.rewritten_count}")

    for warning in result.warnings:
        print(f"[WARN] {warning}")

    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
