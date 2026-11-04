from __future__ import annotations

import shutil
import sys
from pathlib import Path


MARKER = "// ASCEND PRIVACY DEFAULTS"
PREFS = """\n\n// ASCEND PRIVACY DEFAULTS\npref(\"toolkit.telemetry.enabled\", false);\npref(\"toolkit.telemetry.unified\", false);\npref(\"datareporting.healthreport.uploadEnabled\", false);\npref(\"datareporting.policy.dataSubmissionEnabled\", false);\npref(\"app.shield.optoutstudies.enabled\", false);\npref(\"browser.newtabpage.activity-stream.showSponsored\", false);\npref(\"browser.newtabpage.activity-stream.showSponsoredTopSites\", false);\npref(\"browser.newtabpage.activity-stream.feeds.section.topstories\", false);\npref(\"browser.newtabpage.activity-stream.telemetry\", false);\npref(\"browser.discovery.enabled\", false);\npref(\"privacy.trackingprotection.enabled\", true);\npref(\"privacy.trackingprotection.pbmode.enabled\", true);\npref(\"toolkit.legacyUserProfileCustomizations.stylesheets\", true);\n"""
POLICIES = """{
  "policies": {
    "DisableTelemetry": true,
    "DisableFirefoxStudies": true,
    "ExtensionSettings": {
      "uBlock0@raymondhill.net": {
        "installation_mode": "force_installed",
        "install_url": "https://addons.mozilla.org/firefox/downloads/latest/ublock-origin/latest.xpi"
      }
    }
  }
}
"""


def apply(source: Path) -> None:
    pref_file = source / "browser" / "app" / "profile" / "firefox.js"
    if not pref_file.is_file():
        raise FileNotFoundError(f"Firefox default preference file not found: {pref_file}")
    text = pref_file.read_text(encoding="utf-8")
    if MARKER not in text:
        text = text.rstrip() + "\n\n" + MARKER + "\n"
    missing_preferences = [
        line for line in PREFS.splitlines()
        if line.startswith("pref(") and line not in text
    ]
    if missing_preferences:
        text = text.rstrip() + "\n" + "\n".join(missing_preferences) + "\n"
    pref_file.write_text(text, encoding="utf-8", newline="\n")

    browser_prefs = source / "browser" / "app" / "profile" / "firefox.js"
    text = browser_prefs.read_text(encoding="utf-8")
    text = text.replace(
        'pref("browser.startup.homepage",            "about:home");',
        'pref("browser.startup.homepage",            "chrome://browser/content/ascend-start.html");',
    )
    browser_prefs.write_text(text, encoding="utf-8", newline="\n")

    browser_config = source / "browser" / "moz.configure"
    config_text = browser_config.read_text(encoding="utf-8")
    config_text = config_text.replace(
        'imply_option("MOZ_APP_VENDOR", "Mozilla")',
        'imply_option("MOZ_APP_VENDOR", "Ascend")',
    )
    config_text = config_text.replace(
        'imply_option("MOZ_APP_ID", "{ec8030f7-c20a-464f-9b0e-13a3a9e97384}")',
        'imply_option("MOZ_APP_ID", "{9f8185ee-7c36-4e68-8820-277e7a0c4e96}")',
    )
    browser_config.write_text(config_text, encoding="utf-8", newline="\n")

    start_page = Path(__file__).resolve().parents[1] / "profile-template" / "startpage.html"
    bundled_start_page = source / "browser" / "base" / "content" / "ascend-start.html"
    shutil.copy2(start_page, bundled_start_page)
    browser_jar = source / "browser" / "base" / "jar.mn"
    jar_text = browser_jar.read_text(encoding="utf-8")
    jar_entry = "        content/browser/ascend-start.html                 (content/ascend-start.html)\n"
    if "content/browser/ascend-start.html" not in jar_text:
        anchor = "*       content/browser/browser.xhtml                 (content/browser.xhtml)\n"
        if anchor not in jar_text:
            raise RuntimeError("Firefox browser jar manifest changed; cannot package the Ascend start page")
        browser_jar.write_text(jar_text.replace(anchor, anchor + jar_entry, 1), encoding="utf-8", newline="\n")

    chrome_css = source / "browser" / "themes" / "shared" / "browser-shared.css"
    css_marker = "/* ASCEND DARK CHROME */"
    css = chrome_css.read_text(encoding="utf-8")
    if css_marker not in css:
        custom_chrome = (Path(__file__).resolve().parents[1] / "profile-template" / "userChrome.css").read_text(encoding="utf-8")
        chrome_css.write_text(css.rstrip() + "\n\n" + css_marker + "\n" + custom_chrome, encoding="utf-8", newline="\n")

    distribution = source / "browser" / "app" / "distribution"
    (distribution / "policies.json").write_text(POLICIES, encoding="utf-8", newline="\n")
    distribution_build = source / "browser" / "app" / "distribution" / "moz.build"
    distribution_text = distribution_build.read_text(encoding="utf-8")
    policy_entry = 'FINAL_TARGET_FILES.distribution += [\n    "policies.json",\n]\n'
    if '"policies.json"' not in distribution_text:
        distribution_build.write_text(distribution_text.rstrip() + "\n\n" + policy_entry, encoding="utf-8", newline="\n")
    package_manifest = source / "browser" / "installer" / "package-manifest.in"
    manifest_text = package_manifest.read_text(encoding="utf-8")
    manifest_entry = "@RESPATH@/distribution/policies.json"
    if manifest_entry not in manifest_text:
        marker = "#if defined(BUILT_BY_MOZILLA)\n@RESPATH@/distribution/*"
        if marker not in manifest_text:
            raise RuntimeError("Firefox package manifest changed; cannot add Ascend enterprise policies safely")
        package_manifest.write_text(
            manifest_text.replace(marker, manifest_entry + "\n\n" + marker, 1),
            encoding="utf-8",
            newline="\n",
        )

    original = source / "browser" / "branding" / "unofficial"
    branded = source / "browser" / "branding" / "ascend"
    if not original.is_dir():
        raise FileNotFoundError(f"Firefox unofficial branding assets not found: {original}")
    if branded.exists():
        shutil.rmtree(branded)
    shutil.copytree(original, branded)

    for path in branded.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".sh", ".ftl", ".properties", ".dtd", ".txt", ".xml"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        text = text.replace("Firefox Developer Edition", "Ascend Browser")
        text = text.replace("Firefox Nightly", "Ascend Browser")
        text = text.replace("Nightly", "Ascend Browser")
        text = text.replace("Firefox", "Ascend Browser")
        path.write_text(text, encoding="utf-8", newline="\n")

    installer_branding = branded / "branding.nsi"
    if installer_branding.is_file():
        text = installer_branding.read_text(encoding="utf-8")
        text = text.replace('BrandFullNameInternal "Mozilla Developer Preview"', 'BrandFullNameInternal "Ascend Browser"')
        text = text.replace('BrandFullName         "Mozilla Developer Preview"', 'BrandFullName         "Ascend Browser"')
        text = text.replace('CompanyName           "mozilla.org"', 'CompanyName           "Ascend Browser Project"')
        text = text.replace('Channel "unofficial"', 'Channel "ascend"')
        text = text.replace('COMMON_BACKGROUND_COLOR 0x000000', 'COMMON_BACKGROUND_COLOR 0x0B1018')
        text = text.replace('!define AppName               "Firefox"', '!define AppName               "Ascend"')
        text = text.replace('!define DDEApplication        "Firefox"', '!define DDEApplication        "Ascend"')
        text = text.replace('!define AppRegName            "Firefox"', '!define AppRegName            "Ascend"')
        text = text.replace('!define BrandProductName      "Firefox"', '!define BrandProductName      "Ascend Browser"')
        installer_branding.write_text(text, encoding="utf-8", newline="\n")

    installer_defines = source / "browser" / "installer" / "windows" / "nsis" / "defines.nsi.in"
    text = installer_defines.read_text(encoding="utf-8")
    for source_line, ascend_line in (
        ('!define AppName               "Firefox"', '!define AppName               "Ascend"'),
        ('!define DDEApplication        "Firefox"', '!define DDEApplication        "Ascend"'),
        ('!define AppRegName            "Firefox"', '!define AppRegName            "Ascend"'),
        ('!define BrandProductName      "Firefox"', '!define BrandProductName      "Ascend Browser"'),
    ):
        if ascend_line not in text and source_line in text:
            text = text.replace(source_line, ascend_line, 1)
    installer_defines.write_text(text, encoding="utf-8", newline="\n")

    custom_assets = Path(__file__).resolve().parents[1] / "branding"
    for asset in custom_assets.iterdir():
        if asset.is_file():
            shutil.copy2(asset, branded / asset.name)

    configure = branded / "configure.sh"
    if configure.is_file():
        text = configure.read_text(encoding="utf-8")
        text = text.replace("MOZ_APP_DISPLAYNAME=Ascend Browser", 'MOZ_APP_DISPLAYNAME="Ascend Browser"')
        text = text.replace('MOZ_APP_DISPLAYNAME="Firefox Developer Edition"', 'MOZ_APP_DISPLAYNAME="Ascend Browser"')
        text = text.replace('MOZ_APP_DISPLAYNAME="Firefox"', 'MOZ_APP_DISPLAYNAME="Ascend Browser"')
        text = text.replace("MOZ_MACBUNDLE_ID=nightlyunofficial", "MOZ_MACBUNDLE_ID=org.ascend.browser")
        configure.write_text(text, encoding="utf-8", newline="\n")

    mozconfig = source / "mozconfig"
    mozconfig.write_text(
        "# Ascend Browser release-style build; keep Gecko security defaults intact.\n"
        "mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/obj-ascend\n"
        "mk_add_options MOZ_PARALLEL_BUILD=2\n"
        "ac_add_options --enable-project=browser\n"
        "ac_add_options --with-app-basename=Ascend\n"
        "ac_add_options --with-app-name=ascend\n"
        "ac_add_options --with-branding=browser/branding/ascend\n"
        "ac_add_options --with-redist\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: apply_ascend.py <firefox-source-directory>")
    apply(Path(sys.argv[1]).resolve())
