from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


APP = Path(__file__).resolve().parent
SOURCE = APP / "firefox-source"
GIT = os.environ.get("GIT_EXECUTABLE") or shutil.which("git") or "git"
PATCHER = APP / "patches" / "apply_ascend.py"


def run(*args: str) -> None:
    subprocess.run([GIT, *args], cwd=SOURCE, check=True)


def main() -> int:
    if not (SOURCE / ".git").is_dir():
        print("Firefox source is not installed. Run Install first.", file=sys.stderr)
        return 1
    print("Refreshing the generated Firefox checkout. Local edits inside app/firefox-source are discarded; keep Ascend changes in app/patches.")
    run("fetch", "--depth", "1", "origin", "main")
    run("reset", "--hard", "origin/main")
    subprocess.run([sys.executable, str(PATCHER), str(SOURCE)], check=True)
    (APP / "user-data" / "mozilla-bootstrap-complete").unlink(missing_ok=True)
    print("Firefox source updated and Ascend defaults reapplied. Build again before launching the fork.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
