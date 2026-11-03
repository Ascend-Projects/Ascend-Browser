module.exports = {
  run: [
    {
      when: "{{!exists('app/MozillaBuildSetup-4.2.1.exe')}}",
      method: "fs.download",
      params: {
        uri: "https://ftp.mozilla.org/pub/mozilla/libraries/win32/MozillaBuildSetup-4.2.1.exe",
        path: "app/MozillaBuildSetup-4.2.1.exe"
      }
    },
    {
      method: "shell.run",
      params: {
        path: "app",
        env: {
          GIT_EXECUTABLE: "{{which('git')}}"
        },
        message: "{{which('python')}} setup.py"
      }
    }
  ]
}
