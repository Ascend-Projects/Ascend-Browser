// ascend-core/src/main.rs

use std::env;
use std::process;

fn main() {
    // Set environment variables to enforce privacy and security
    env::set_var("MOZ_TELEMETRY_REPORTING", "false");
    env::set_var("MOZ_SAFE_BROWSING_ENABLED", "true");
    env::set_var("CAPTIVE_PORTAL_SERVICE_URL", "");
    env::set_var("XRE_DISABLE_UPDATE_DIALOG", "1");

    // Path to the Firefox binary
    let firefox_binary_path = env::var("ASCEND_FIREFOX_BINARY").unwrap_or_else(|_| {
        panic!("Environment variable ASCEND_FIREFOX_BINARY is not set");
    });

    // Launch Firefox with custom user.js and policies.json
    let args = vec![
        "firefox.exe",
        "-userprofile",
        &ascend_profile::get_user_profile_path(),
        "--no-remote",
        "--new-instance",
        "--chrome",
        "-url",
        "about:blank",
        "-width",
        "800",
        "-height",
        "600",
        "-jsloader",
        ascend_core::user_js_path().to_str().unwrap(),
        "-policies",
        ascend_core::policies_json_path().to_str().unwrap(),
    ];

    process::Command::new(&firefox_binary_path)
        .args(args)
        .spawn()
        .expect("Failed to launch Firefox");

    println!("Firefox launched successfully.");
}
