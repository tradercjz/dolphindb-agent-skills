#!/usr/bin/env python3
"""Build + optionally upload dolphindb-agent-skills to PyPI.

Steps performed:
  1. Sync skills/ → src/dolphindb_skill_installer/skills/  (so wheel bundles them)
  2. Build wheel with `uv build`
  3. Remove the synced copy (keep repo clean)
  4. Optionally upload with twine

Usage:
    # Build only
    uv run upload_to_pypi.py

    # Build and upload
    uv run upload_to_pypi.py --upload
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SKILLS_SRC = ROOT / "skills"
SKILLS_DST = ROOT / "src" / "dolphindb_skill_installer" / "skills"


def sync_skills() -> None:
    print(f"📂 Syncing skills/ → {SKILLS_DST.relative_to(ROOT)}")
    if SKILLS_DST.exists():
        shutil.rmtree(SKILLS_DST)
    shutil.copytree(SKILLS_SRC, SKILLS_DST)
    print("   ✅ Done")


def clean_skills() -> None:
    if SKILLS_DST.exists():
        shutil.rmtree(SKILLS_DST)
        print(f"🧹 Removed {SKILLS_DST.relative_to(ROOT)}")


def build() -> None:
    print("\n🔨 Building wheel with python -m build …")
    result = subprocess.run([sys.executable, "-m", "build", "--no-isolation"], cwd=ROOT)
    if result.returncode != 0:
        print("❌ Build failed")
        sys.exit(result.returncode)
    print("   ✅ Build complete — artifacts in dist/")


def upload() -> None:
    print("\n🚀 Uploading to PyPI with twine …")
    result = subprocess.run(
        ["python", "-m", "twine", "upload", "dist/*"], cwd=ROOT
    )
    if result.returncode != 0:
        print("❌ Upload failed")
        sys.exit(result.returncode)
    print("   ✅ Upload complete")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--upload", action="store_true",
                        help="Upload to PyPI after building (requires twine)")
    args = parser.parse_args()

    try:
        sync_skills()
        build()
    finally:
        clean_skills()

    if args.upload:
        upload()


if __name__ == "__main__":
    main()
