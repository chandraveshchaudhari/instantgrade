"""Utility: build a docker image for instantgrade tagged by current git SHA.

Usage:
    python tools/docker_build_image.py [--force]

This mirrors the behavior used by the ExecutionServiceDocker to ensure images are
unique per commit. Use --force to rebuild even if image already exists.
"""
import subprocess
import sys
from pathlib import Path

def get_git_sha(repo_root: Path) -> str:
    try:
        out = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=repo_root, text=True)
        return out.strip()
    except Exception:
        return "latest"


def image_exists(tag: str) -> bool:
    try:
        res = subprocess.run(["docker", "images", "-q", tag], capture_output=True, text=True)
        return bool(res.stdout.strip())
    except Exception:
        return False


def build_image(repo_root: Path, tag: str) -> None:
    dockerfile = repo_root / "Dockerfile" if (repo_root / "Dockerfile").exists() else None
    build_context = repo_root
    cmd = ["docker", "build", "-t", tag, str(build_context)]
    if dockerfile:
        cmd = ["docker", "build", "-t", tag, "-f", str(dockerfile), str(build_context)]
    print("Running:", " ".join(cmd))
    subprocess.check_call(cmd)
    # tag latest as convenience
    try:
        subprocess.check_call(["docker", "tag", tag, "instantgrade:latest"])
    except Exception:
        pass


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[1]
    force = "--force" in sys.argv or "-f" in sys.argv
    sha = get_git_sha(repo_root)
    tag = f"instantgrade:{sha}"

    if image_exists(tag) and not force:
        print(f"Image {tag} already exists. Use --force to rebuild.")
        sys.exit(0)

    print(f"Building image {tag} from {repo_root} (force={force})")
    build_image(repo_root, tag)
    print("Done.")
