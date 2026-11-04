from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


APP = Path(__file__).resolve().parent
SOURCE = APP / "firefox-source"
PATCHER = APP / "patches" / "apply_ascend.py"
MOZILLA_BUILD = Path(os.environ.get("MOZILLABUILD", r"C:\mozilla-build"))
INSTALLER = APP / "MozillaBuildSetup-4.2.1.exe"
GIT = os.environ.get("GIT_EXECUTABLE") or shutil.which("git") or "git"


def run(command: list[str], *, cwd: Path | None = None) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def main() -> int:
    if sys.platform != "win32":
        print("This first Ascend source build targets Windows x64.", file=sys.stderr)
        return 1

    if not (MOZILLA_BUILD / "start-shell.bat").is_file():
        if not INSTALLER.is_file():
            print("MozillaBuild installer is missing. Run Install again.", file=sys.stderr)
            return 1
        print("Installing MozillaBuild to its documented default location...")
        run([str(INSTALLER), "/S"])
        if not (MOZILLA_BUILD / "start-shell.bat").is_file():
            print("MozillaBuild setup did not create start-shell.bat.", file=sys.stderr)
            return 1

    if not (SOURCE / ".git").is_dir():
        print("Cloning the official Mozilla Firefox source tree (about 1 GB of Git data)...")
        run([GIT, "clone", "--depth", "1", "https://github.com/mozilla-firefox/firefox.git", str(SOURCE)], cwd=APP)

    if not (SOURCE / "mach").is_file():
        print("Firefox source checkout is incomplete. Run Install again after removing the incomplete checkout.", file=sys.stderr)
        return 1

    APP.joinpath("user-data").mkdir(parents=True, exist_ok=True)
    run([sys.executable, str(PATCHER), str(SOURCE)])
    print("Ascend source is ready. Use Build from source to configure and compile the browser.")
    print("The first build is interactive and can take hours. Choose Firefox Desktop in Mozilla's bootstrap prompts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
