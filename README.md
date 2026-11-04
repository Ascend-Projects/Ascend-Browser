# Ascend Browser

Ascend is an independent Windows/Linux/Mac desktop browser built from Mozilla's Gecko source. It uses its own `ascend.exe`, installer, product identity, profile, icon set, dark browser chrome, and branded start page. It does not launch an installed Firefox. Gecko handles web rendering, site isolation, sandboxing, certificates, and browser security.

## Run and build

Also runnable with your AI agent

## Ascend design and defaults

- Graphite and midnight browser chrome, rounded tabs and address field, teal focus accents, and compact spacing.
- A local start page with the Ascend compass mark and DuckDuckGo search. It loads no remote images or scripts.
- Custom browser, private-window, tab, and Windows installer artwork and Ascend product names.
- Telemetry, health uploads, studies, sponsored new-tab content, and recommendations disabled by default.
- Tracking protection enabled, plus the Firefox enterprise policy to install signed uBlock Origin from AMO and receive extension updates.

The signed uBlock Origin extension is installed from AMO on first browser launch when network access is available. Privacy preferences do not guarantee zero network requests; verify traffic before making that claim.

## Update and reset

**No new updates yet**

## Programmatic interface

Ascend is a desktop browser, not a local HTTP service. It does not currently expose a supported browser-control API for JavaScript, Python, or Curl. Web pages can use standard browser APIs such as `fetch()`; Python `requests` and Curl can access websites directly, but those are not Ascend APIs. Remote debugging is not enabled by default.
