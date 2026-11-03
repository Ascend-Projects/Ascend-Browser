# Ascend Browser

Ascend is an independent Windows desktop browser built from Mozilla's Gecko source. It uses its own `ascend.exe`, installer, product identity, profile, icon set, dark browser chrome, and branded start page. It does not launch an installed Firefox. Gecko handles web rendering, site isolation, sandboxing, certificates, and browser security.

## Run and build

1. In Pinokio, choose **Install** to install MozillaBuild when needed and fetch Mozilla's browser source into `app/firefox-source`.
2. Choose **Build Ascend Browser** and select Firefox Desktop during Mozilla's first-run bootstrap. The two-job build creates Ascend's own `ascend.exe` and a full Windows installer.
3. The installer is published as `dist/Ascend-Browser-Setup.exe`. Run it to install Ascend into Windows, or use **Start Ascend** in Pinokio after the build completes.
4. Ascend keeps its browser profile in `app/user-data/profile`, separate from any Firefox profile on the machine.
5. **Reset build output** runs `mach clobber`; it keeps the source and Ascend profile.

The first Firefox build can take hours and requires Windows 10/11 x64, MozillaBuild, and substantial free disk space. This launcher currently targets Windows x64. The generated source tree, profile, and installer are local files excluded from Git. A locally built installer is unsigned; Windows may show a publisher warning.

## Ascend design and defaults

- Graphite and midnight browser chrome, rounded tabs and address field, teal focus accents, and compact spacing.
- A local start page with the Ascend compass mark and DuckDuckGo search. It loads no remote images or scripts.
- Custom browser, private-window, tab, and Windows installer artwork and Ascend product names.
- Telemetry, health uploads, studies, sponsored new-tab content, and recommendations disabled by default.
- Tracking protection enabled, plus the Firefox enterprise policy to install signed uBlock Origin from AMO and receive extension updates.

The signed uBlock Origin extension is installed from AMO on first browser launch when network access is available. Privacy preferences do not guarantee zero network requests; verify traffic before making that claim.

## Update and reset

**Update Firefox source** fetches the latest upstream `main`, resets the local source checkout to it, and reapplies the Ascend patch. Keep custom work in `app/patches` and `app/branding`; edits made directly in `app/firefox-source` are discarded by this action. Then run **Build from source** again. **Reset build output** removes generated build products through Mozilla's `mach clobber` command.

## Programmatic interface

Ascend is a desktop browser, not a local HTTP service. It does not currently expose a supported browser-control API for JavaScript, Python, or Curl. Web pages can use standard browser APIs such as `fetch()`; Python `requests` and Curl can access websites directly, but those are not Ascend APIs. Remote debugging is not enabled by default.

## References

- [Mozilla Firefox Windows build guide](https://firefox-source-docs.mozilla.org/setup/windows_build.html)
- [Mozilla Windows installer build guide](https://firefox-source-docs.mozilla.org/browser/installer/windows/installer/InstallerBuild.html)
- [Firefox build options](https://firefox-source-docs.mozilla.org/setup/configuring_build_options.html)
- [Firefox process model](https://firefox-source-docs.mozilla.org/dom/ipc/process_model.html)
- [Firefox enterprise policies](https://mozilla.github.io/policy-templates/)
