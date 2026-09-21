#!/usr/bin/env python3
"""
将 Hugo 文章 .md 文件转换为 Page Bundle 文件夹格式。
每个 xxx.md 变成 xxx/index.md。
"""

import os
import sys
import shutil
import argparse
from pathlib import Path


def convert_to_page_bundles(source_dir, dest_dir=None, recursive=False, dry_run=False):
    source = Path(source_dir).resolve()
    if dest_dir:
        dest = Path(dest_dir).resolve()
    else:
        dest = source

    if not source.is_dir():
        print(f"❌ 错误：源目录不存在或不是目录：{source}")
        sys.exit(1)

    if dest != source:
        dest.mkdir(parents=True, exist_ok=True)

    # 收集所有 .md 文件
    if recursive:
        md_files = list(source.rglob("*.md"))
    else:
        md_files = list(source.glob("*.md"))

    if not md_files:
        print("ℹ️ 没有找到任何 .md 文件")
        return

    processed = 0
    skipped = 0

    for md_file in md_files:
        # 如果文件本身就是 index.md，说明可能已经是 Page Bundle，跳过
        if md_file.name == "index.md":
            print(f"⏭️  跳过 {md_file}（已经是 index.md）")
            skipped += 1
            continue

        folder_name = md_file.stem  # 去掉 .md 的文件名
        target_folder = dest / folder_name
        target_index = target_folder / "index.md"

        # 如果目标文件夹已存在且里面已有 index.md，跳过，避免覆盖
        if target_index.exists():
            print(f"⏭️  跳过 {md_file}：目标 {target_index} 已存在")
            skipped += 1
            continue

        print(f"📄 处理：{md_file}  ->  {target_index}")
        if dry_run:
            continue

        # 创建文件夹并移动文件
        target_folder.mkdir(parents=True, exist_ok=True)
        shutil.move(str(md_file), str(target_index))
        processed += 1

    print(f"\n✅ 完成！共处理 {processed} 个文件，跳过 {skipped} 个。")
    if dry_run:
        print("⚠️  这是预览模式（--dry-run），未实际修改任何文件。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="将 Hugo 文章 .md 文件转换为 Page Bundle 文件夹格式"
    )
    parser.add_argument(
        "source",
        nargs="?",
        default=".",
        help="源目录，默认为当前目录"
    )
    parser.add_argument(
        "-d", "--dest",
        help="目标目录，默认为源目录"
    )
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="递归处理子目录"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅预览，不实际执行"
    )
    args = parser.parse_args()

    convert_to_page_bundles(
        args.source,
        args.dest,
        args.recursive,
        args.dry_run
    )