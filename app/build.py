from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


APP = Path(__file__).resolve().parent
SOURCE = APP / "firefox-source"
MOZILLA_BUILD = Path(os.environ.get("MOZILLABUILD", r"C:\mozilla-build"))
SHELL = MOZILLA_BUILD / "start-shell.bat"
PATCHER = APP / "patches" / "apply_ascend.py"
BOOTSTRAP_MARKER = APP / "user-data" / "mozilla-bootstrap-complete"
INSTALLER = APP.parent / "dist" / "Ascend-Browser-Setup.exe"


def run_mozilla(command: str) -> int:
    if not SHELL.is_file():
        print(f"MozillaBuild shell not found: {SHELL}. Run Install first.", file=sys.stderr)
        return 1
    env = os.environ.copy()
    env["USE_MINTTY"] = "0"
    env["MOZCONFIG"] = str(SOURCE / "mozconfig")
    wrapper = APP / "user-data" / "run-mozilla-command.cmd"
    wrapper.parent.mkdir(parents=True, exist_ok=True)
    wrapper.write_text(
        "@echo off\r\n"
        f'call "{SHELL}" -no-start -defterm -full-path -c "{command}"\r\n'
        "exit /b %ERRORLEVEL%\r\n",
        encoding="utf-8",
        newline="",
    )
    command_line = f'"{os.environ.get("COMSPEC", "cmd.exe")}" /d /c "{wrapper}"'
    return subprocess.run(command_line, cwd=SOURCE, env=env).returncode


def publish_installer() -> bool:
    candidates = sorted(
        (SOURCE / "obj-ascend" / "dist").rglob("*.installer.exe"),
        key=lambda candidate: candidate.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        print("Firefox package completed, but no full Windows installer .exe was produced.", file=sys.stderr)
        return False
    INSTALLER.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(candidates[0], INSTALLER)
    print(f"Installable Ascend Browser created: {INSTALLER}")
    return True


def main() -> int:
    if sys.platform != "win32":
        print("The configured Ascend build currently targets Windows x64.", file=sys.stderr)
        return 1
    if not (SOURCE / "mach").is_file():
        print("Firefox source is not installed. Run Install first.", file=sys.stderr)
        return 1
    subprocess.run([sys.executable, str(PATCHER), str(SOURCE)], check=True)

    if "--clobber" in sys.argv:
        return run_mozilla("./mach clobber")

    if not BOOTSTRAP_MARKER.is_file():
        print("Mozilla bootstrap will prompt for a build type. Choose Firefox Desktop; a full source build is required for Ascend branding and defaults.")
        code = run_mozilla("./mach bootstrap")
        if code != 0:
            return code
        BOOTSTRAP_MARKER.parent.mkdir(parents=True, exist_ok=True)
        BOOTSTRAP_MARKER.write_text("complete\n", encoding="utf-8")

    code = run_mozilla("./mach build && ./mach package")
    if code == 0:
        return 0 if publish_installer() else 1
    return code


if __name__ == "__main__":
    raise SystemExit(main())
