use std::env;
use std::fs;
use std::process::Command;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Set environment variables to enforce privacy and security at runtime
    env::set_var("MOZ_TELEMETRY_REPORTING", "false");
    env::set_var("MOZ_SAFE_BROWSING_ENABLED", "true");
    env::set_var("CAPTIVE_PORTAL_SERVICE_URL", "");
    env::set_var("XRE_DISABLE_UPDATE_DIALOG", "1");

    let current_dir = env::current_dir()?;
    let firefox_binary_path = current_dir.join("firefox.exe");
    let profile_dir = current_dir.join("ascend-profile");

    // Ensure isolated profile directory exists
    if !profile_dir.exists() {
        fs::create_dir_all(&profile_dir)?;
    }

    // Embed configs at compile time and seed them into the isolated profile directory
    let user_js_content = include_str!("../../ascend-profile/user.js");
    let policies_json_content = include_str!("../../ascend-profile/policies.json");

    fs::write(profile_dir.join("user.js"), user_js_content)?;
    fs::write(profile_dir.join("policies.json"), policies_json_content)?;
    println!("[Ascend Core] Hardened user.js and policies injected into profile.");

    if !firefox_binary_path.exists() {
        panic!("Firefox binary not found at: {:?}. Did you run the installer first?", firefox_binary_path);
    }

    println!("[Ascend Core] Launching Ascend Browser...");

    // Launch Firefox cleanly with isolated profile arguments
    let status = Command::new(&firefox_binary_path)
        .arg("-profile")
        .arg(&profile_dir)
        .arg("--no-remote")
        .arg("--new-instance")
        .status();

    match status {
        Ok(exit_status) => println!("Browser exited with status: {}", exit_status),
        Err(err) => eprintln!("Failed to launch browser process: {}", err),
    }

    Ok(())
}