module.exports = {
  daemon: true,
  run: [{
    method: "shell.run",
    params: {
      path: "app",
      message: "{{which('python')}} start_browser.py"
    }
  }]
}
