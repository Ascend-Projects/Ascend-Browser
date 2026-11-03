module.exports = {
  run: [{
    method: "shell.run",
    params: {
      input: true,
      path: "app",
      message: "{{which('python')}} build.py"
    }
  }]
}
