
use std::fs;
use std::path::{Path, PathBuf};

pub fn get_user_profile_path() -> String {
    let base_dir = env::var("ASCEND_PROFILE_DIR").unwrap_or_else(|_| "./ascend-profile".to_string());
    fs::create_dir_all(&base_dir).expect("Failed to create profile directory");
    base_dir
}

pub fn user_js_path() -> PathBuf {
    PathBuf::from(format!("{}{}", get_user_profile_path(), "user.js"))
}

pub fn policies_json_path() -> PathBuf {
    PathBuf::from(format!("{}{}", get_user_profile_path(), "policies.json"))
}
