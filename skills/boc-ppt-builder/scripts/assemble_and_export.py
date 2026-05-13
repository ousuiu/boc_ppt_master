#!/usr/bin/env python3
"""Assemble BOC PPT SVG pages and export a PPTX with ppt-master."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from common_svg import (
    build_asset_index,
    extract_page_pairs,
    replace_page_number,
    rewrite_asset_refs_in_text,
)
from validate_chapters import collect_top_level_svgs, discover_chapters, validate_asset_refs


@dataclass(frozen=True)
class SlideSource:
    kind: str
    source: Path
    chapter_number: int | None = None
    content_number: int | None = None


def page_file_number(path: Path) -> int:
    stem = path.stem.lower()
    if stem.startswith("page"):
        return int(stem[4:])
    raise ValueError(f"Not a page file: {path}")


def validate_complete_deck(chapters_dir: Path) -> tuple[list[SlideSource], list[str]]:
    errors: list[str] = []
    chapters, chapter_errors = discover_chapters(chapters_dir)
    errors.extend(chapter_errors)

    required = {
        "cover": chapters_dir / "cover.svg",
        "toc": chapters_dir / "toc.svg",
        "ending": chapters_dir / "ending.svg",
    }
    for label, path in required.items():
        if not path.exists():
            errors.append(f"Missing required {label} SVG: {path}")

    expected_chapter_numbers = {chapter.number for chapter in chapters}
    chapter_svg_paths = sorted(chapters_dir.glob("chapter*.svg"), key=lambda item: item.name.lower())
    found_chapter_numbers: set[int] = set()
    for path in chapter_svg_paths:
        suffix = path.stem[len("chapter") :]
        if not suffix.isdigit():
            errors.append(f"Invalid chapter SVG name: {path.name}. Expected chapter[n].svg.")
            continue
        found_chapter_numbers.add(int(suffix))

    if expected_chapter_numbers and found_chapter_numbers != expected_chapter_numbers:
        errors.append(
            "chapter[n].svg files do not match chapter folders: "
            f"found {sorted(found_chapter_numbers)}, expected {sorted(expected_chapter_numbers)}."
        )

    svg_paths: list[Path] = []
    for path in required.values():
        if path.exists():
            svg_paths.append(path)
    svg_paths.extend(chapter_svg_paths)
    for chapter in chapters:
        svg_paths.extend(chapter.pages)

    asset_errors, _, _ = validate_asset_refs(svg_paths, chapters_dir / "asset", fix_assets=False)
    errors.extend(asset_errors)

    if errors:
        return [], errors

    slides: list[SlideSource] = [
        SlideSource(kind="cover", source=required["cover"]),
        SlideSource(kind="toc", source=required["toc"]),
    ]

    for chapter in chapters:
        slides.append(
            SlideSource(
                kind="chapter",
                source=chapters_dir / f"chapter{chapter.number}.svg",
                chapter_number=chapter.number,
            )
        )
        for page in sorted(chapter.pages, key=page_file_number):
            slides.append(
                SlideSource(
                    kind="content",
                    source=page,
                    chapter_number=chapter.number,
                    content_number=page_file_number(page),
                )
            )

    slides.append(SlideSource(kind="ending", source=required["ending"]))
    return slides, []


def clean_svg_dir(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    for svg_path in directory.glob("*.svg"):
        svg_path.unlink()


def target_name(slide: SlideSource, page_num: int, width: int) -> str:
    prefix = f"{page_num:0{width}d}"
    if slide.kind == "chapter":
        return f"{prefix}_chapter{slide.chapter_number}.svg"
    if slide.kind == "content":
        return f"{prefix}_content{slide.content_number}.svg"
    return f"{prefix}_{slide.kind}.svg"


def processed_svg_text(
    source: Path,
    target: Path,
    asset_index: dict[str, list[Path]],
    page_num: int,
    total_pages: int,
    add_page_number: bool,
) -> tuple[str, int]:
    text = source.read_text(encoding="utf-8")
    asset_result = rewrite_asset_refs_in_text(text, target, asset_index)
    if asset_result.missing:
        raise RuntimeError(f"{source} has missing assets: {', '.join(asset_result.missing)}")
    text, page_replacement_count = replace_page_number(
        asset_result.text,
        page_num=page_num,
        total_pages=total_pages,
        add_if_missing=add_page_number,
    )
    return text, asset_result.rewritten_count + page_replacement_count


def organize_svgs(chapters_dir: Path, slides: list[SlideSource], add_page_number: bool) -> tuple[int, int]:
    final_dir = chapters_dir / "final_svg"
    output_dir = chapters_dir / "output_svg"
    clean_svg_dir(final_dir)
    clean_svg_dir(output_dir)

    asset_index = build_asset_index(chapters_dir / "asset")
    total_pages = len(slides)
    width = max(2, len(str(total_pages)))
    rewrite_count = 0

    for index, slide in enumerate(slides, start=1):
        name = target_name(slide, index, width)
        for target_dir in (final_dir, output_dir):
            target = target_dir / name
            text, count = processed_svg_text(
                source=slide.source,
                target=target,
                asset_index=asset_index,
                page_num=index,
                total_pages=total_pages,
                add_page_number=add_page_number,
            )
            target.write_text(text, encoding="utf-8")
            rewrite_count += count

    return total_pages, rewrite_count


def repair_output_page_numbers(output_dir: Path, total_pages: int, add_page_number: bool) -> list[str]:
    errors: list[str] = []
    files = sorted(output_dir.glob("*.svg"))
    if len(files) != total_pages:
        errors.append(f"output_svg contains {len(files)} SVG files, expected {total_pages}.")

    for path in files:
        try:
            page_num = int(path.name.split("_", 1)[0])
        except ValueError:
            errors.append(f"Output SVG does not start with a page number: {path.name}")
            continue

        text = path.read_text(encoding="utf-8")
        pairs = extract_page_pairs(text)
        if pairs and all(pair == (page_num, total_pages) for pair in pairs):
            continue

        text, _ = replace_page_number(
            text,
            page_num=page_num,
            total_pages=total_pages,
            add_if_missing=add_page_number,
        )
        path.write_text(text, encoding="utf-8")

        pairs = extract_page_pairs(text)
        if not pairs:
            errors.append(f"No page number found or inserted in {path.name}.")
        elif not all(pair == (page_num, total_pages) for pair in pairs):
            errors.append(f"Page number still mismatches in {path.name}: found {pairs}.")

    return errors


def run_export(project_root: Path, chapters_dir: Path, quiet: bool) -> None:
    ppt_master_script = project_root / "ppt-master" / "skills" / "ppt-master" / "scripts" / "svg_to_pptx.py"
    if not ppt_master_script.exists():
        raise FileNotFoundError(f"Missing ppt-master export script: {ppt_master_script}")

    output_dir = chapters_dir / "output_pptx"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_pptx = output_dir / "output.pptx"

    command = [
        sys.executable,
        str(ppt_master_script),
        str(chapters_dir),
        "-s",
        "output_svg",
        "-o",
        str(output_pptx),
    ]
    if quiet:
        command.append("-q")

    subprocess.run(command, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Assemble ppt_chapters SVGs and export a PPTX.")
    parser.add_argument("--project-root", default=str(Path.cwd()), help="Project root, default: current directory.")
    parser.add_argument("--chapters-dir", default=None, help="Explicit ppt_chapters path.")
    parser.add_argument("--skip-export", action="store_true", help="Organize SVGs and repair page numbers without exporting PPTX.")
    parser.add_argument(
        "--no-add-page-number",
        action="store_true",
        help="Do not insert page numbers into SVGs that lack an existing page-number node.",
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="Reduce export logging.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    chapters_dir = Path(args.chapters_dir).resolve() if args.chapters_dir else project_root / "ppt_chapters"

    slides, errors = validate_complete_deck(chapters_dir)
    if errors:
        print("[ERROR] Cannot assemble PPT:")
        for error in errors:
            print(f"  - {error}")
        return 1

    total_pages, rewrite_count = organize_svgs(
        chapters_dir=chapters_dir,
        slides=slides,
        add_page_number=not args.no_add_page_number,
    )
    page_errors = repair_output_page_numbers(
        output_dir=chapters_dir / "output_svg",
        total_pages=total_pages,
        add_page_number=not args.no_add_page_number,
    )
    if page_errors:
        print("[ERROR] Page-number repair failed:")
        for error in page_errors:
            print(f"  - {error}")
        return 1

    print("[OK] SVG assembly completed.")
    print(f"  Total pages: {total_pages}")
    print(f"  SVG edits applied: {rewrite_count}")
    print(f"  final_svg: {chapters_dir / 'final_svg'}")
    print(f"  output_svg: {chapters_dir / 'output_svg'}")

    if args.skip_export:
        print("[OK] Export skipped by --skip-export.")
        return 0

    try:
        run_export(project_root=project_root, chapters_dir=chapters_dir, quiet=args.quiet)
    except subprocess.CalledProcessError as exc:
        print(f"[ERROR] PPTX export failed with exit code {exc.returncode}.")
        return exc.returncode
    except Exception as exc:
        print(f"[ERROR] PPTX export failed: {exc}")
        return 1

    print(f"[OK] PPTX exported: {chapters_dir / 'output_pptx' / 'output.pptx'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
