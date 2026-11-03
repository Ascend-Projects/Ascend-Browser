module.exports = {
  version: "7.0",
  title: "Ascend Browser",
  description: "A private, dark-themed Gecko browser with its own Ascend identity",
  icon: "icon.svg",
  menu: async (kernel, info) => {
    const running = {
      install: info.running("install.js"),
      start: info.running("start.js"),
      build: info.running("build.js"),
      update: info.running("update.js"),
      reset: info.running("reset.js")
    }
    const installed = info.exists("app/firefox-source/.git")

    if (running.install) {
      return [{ default: true, icon: "fa-solid fa-plug", text: "Installing", href: "install.js" }]
    }
    if (!installed) {
      return [{ default: true, icon: "fa-solid fa-plug", text: "Install", href: "install.js" }]
    }
    if (running.build || running.update || running.reset) {
      const action = running.build ? "build" : running.update ? "update" : "reset"
      const text = running.build ? "Building" : running.update ? "Updating source" : "Resetting build"
      return [{ default: true, icon: "fa-solid fa-terminal", text, href: `${action}.js` }]
    }
    if (running.start) {
      return [{ default: true, icon: "fa-solid fa-globe", text: "Browser process", href: "start.js" }]
    }
    const built = info.exists("app/firefox-source/obj-ascend/dist/bin/ascend.exe")
      || info.exists("app/firefox-source/obj-ascend/dist/ascend/ascend.exe")
    if (!built) {
      return [
        { default: true, icon: "fa-solid fa-hammer", text: "Build Ascend Browser", href: "build.js" },
        { icon: "fa-solid fa-rotate", text: "Update Browser Source", href: "update.js" },
        { icon: "fa-solid fa-broom", text: "Reset Build Output", href: "reset.js" }
      ]
    }
    return [
      { default: true, icon: "fa-solid fa-globe", text: "Start Ascend", href: "start.js" },
      { icon: "fa-solid fa-hammer", text: "Rebuild Ascend", href: "build.js" },
      { icon: "fa-solid fa-rotate", text: "Update Browser Source", href: "update.js" },
      { icon: "fa-solid fa-broom", text: "Reset Build Output", href: "reset.js" }
    ]
  }
}
