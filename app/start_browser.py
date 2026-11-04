from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


APP = Path(__file__).resolve().parent
SOURCE = APP / "firefox-source"
PROFILE = APP / "user-data" / "profile"
TEMPLATE = APP / "profile-template"


def custom_build() -> Path | None:
    candidates = [
        SOURCE / "obj-ascend" / "dist" / "bin" / "ascend.exe",
        SOURCE / "obj-ascend" / "dist" / "ascend" / "ascend.exe",
    ]
    return next((candidate for candidate in candidates if candidate.is_file()), None)


def prepare_profile() -> None:
    PROFILE.mkdir(parents=True, exist_ok=True)
    user_js = PROFILE / "user.js"
    chrome = PROFILE / "chrome"
    if not user_js.exists():
        shutil.copy2(TEMPLATE / "user.js", user_js)
    chrome.mkdir(exist_ok=True)
    user_chrome = chrome / "userChrome.css"
    shutil.copy2(TEMPLATE / "userChrome.css", chrome / "ascend-default.css")
    if not user_chrome.exists():
        user_chrome.write_text('@import url("ascend-default.css");\n', encoding="utf-8")
    else:
        current_styles = user_chrome.read_text(encoding="utf-8")
        if "Ascend compact dark browser chrome" in current_styles and '@import url("ascend-default.css");' not in current_styles:
            user_chrome.write_text('@import url("ascend-default.css");\n', encoding="utf-8")
    start_page = PROFILE / "ascend-start.html"
    shutil.copy2(TEMPLATE / "startpage.html", start_page)
    homepage_pref = f'user_pref("browser.startup.homepage", {json.dumps(start_page.as_uri())});\n'
    startup_pref = 'user_pref("browser.startup.page", 1);\n'
    existing = user_js.read_text(encoding="utf-8")
    for line in (homepage_pref, startup_pref):
        if line.split(",", 1)[0] not in existing:
            with user_js.open("a", encoding="utf-8", newline="\n") as profile_config:
                profile_config.write(line)
            existing += line


def main() -> int:
    if sys.platform != "win32":
        print("This launcher currently targets Windows x64.", file=sys.stderr)
        return 1
    browser = custom_build()
    if browser is None:
        print("Ascend's standalone browser has not been built yet. Choose Build from source in Pinokio.", file=sys.stderr)
        return 1

    prepare_profile()
    print(f"Starting the standalone Ascend Browser: {browser}")
    print("Ascend profile: app/user-data/profile (separate from your normal Firefox profile)")
    try:
        return subprocess.run(
            [str(browser), "--no-remote", "--new-instance", "--profile", str(PROFILE)],
            cwd=browser.parent,
            check=False,
        ).returncode
    except OSError as error:
        print(f"Could not start Firefox: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
