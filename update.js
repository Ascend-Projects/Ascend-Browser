module.exports = {
  run: [{
    method: "shell.run",
    params: {
      path: "app",
      env: {
        GIT_EXECUTABLE: "{{which('git')}}"
      },
      message: "{{which('python')}} update_source.py"
    }
  }]
}
