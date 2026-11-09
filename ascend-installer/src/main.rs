use std::fs::{self, File};
use std::io::{self, Write};
use std::path::{Path, PathBuf};
use futures_util::StreamExt;

const FIREFOX_ZIP_URL: &str = "https://ftp.mozilla.org/pub/firefox/releases/128.0esr/win64/en-US/firefox-128.0esr.zip";

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("==================================================");
    println!("     ASCEND BROWSER SYSTEM BOOTSTRAPPER          ");
    println!("==================================================");

    let runtime_dir = PathBuf::from("./ascend-runtime");
    if !runtime_dir.exists() {
        fs::create_dir_all(&runtime_dir)?;
    }

    let archive_path = runtime_dir.join("firefox_core.zip");

    // 1. Download Core Package
    println!("[1/4] Downloading Firefox Core Runtime...");
    let client = reqwest::Client::builder()
        .user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) Ascend/1.0")
        .build()?;

    let res = client.get(FIREFOX_ZIP_URL).send().await?;
    if !res.status().is_success() {
        return Err(format!("Download failed with status: {}", res.status()).into());
    }

    let mut file = File::create(&archive_path)?;
    let mut stream = res.bytes_stream();

    let mut downloaded: u64 = 0;
    while let Some(chunk) = stream.next().await {
        let chunk = chunk?;
        file.write_all(&chunk)?;
        downloaded += chunk.len() as u64;
        print!("\rDownloaded: {:.2} MB", downloaded as f64 / 1_048_576.0);
        io::stdout().flush()?;
    }
    println!("\n[+] Download complete.");

    // 2. Extract Archive
    println!("[2/4] Extracting core runtime binaries...");
    extract_zip(&archive_path, &runtime_dir)?;
    println!("[+] Extraction complete.");

    if archive_path.exists() {
        fs::remove_file(&archive_path)?;
    }

    // 3. Strip Bloat
    println!("[3/4] Stripping telemetry and unnecessary modules...");
    strip_bloat(&runtime_dir)?;

    // 4. Inject Policies
    println!("[4/4] Injecting enterprise lockdown policies...");
    inject_policies(&runtime_dir)?;

    println!("==================================================");
    println!(" SUCCESS: Ascend Browser runtime is assembled!   ");
    println!(" Target directory: ./ascend-runtime               ");
    println!("==================================================");

    Ok(())
}

fn extract_zip(archive: &Path, target: &Path) -> Result<(), Box<dyn std::error::Error>> {
    let file = File::open(archive)?;
    let mut zip = zip::ZipArchive::new(file)?;

    for i in 0..zip.len() {
        let mut file = zip.by_index(i)?;
        let raw_path = match file.enclosed_name() {
            Some(path) => path.to_owned(),
            None => continue,
        };

        let relative_path = if raw_path.starts_with("firefox") {
            raw_path.strip_prefix("firefox").unwrap().to_path_buf()
        } else {
            raw_path
        };

        if relative_path.as_os_str().is_empty() {
            continue;
        }

        let outpath = target.join(relative_path);

        if file.name().ends_with('/') {
            fs::create_dir_all(&outpath)?;
        } else {
            if let Some(p) = outpath.parent() {
                if !p.exists() {
                    fs::create_dir_all(p)?;
                }
            }
            let mut outfile = File::create(&outpath)?;
            io::copy(&mut file, &mut outfile)?;
        }
    }
    Ok(())
}

fn strip_bloat(target: &Path) -> Result<(), Box<dyn std::error::Error>> {
    let remove_list = vec![
        "maintenanceservice.exe",
        "maintenanceservice_installer.exe",
        "pingsender.exe",
        "default-browser-agent.exe",
        "minidump-analyzer.exe",
        "crashreporter.exe",
    ];

    for file in remove_list {
        let path = target.join(file);
        if path.exists() {
            let _ = fs::remove_file(&path);
            println!("  [-] Removed: {}", file);
        }
    }
    Ok(())
}

fn inject_policies(target: &Path) -> Result<(), Box<dyn std::error::Error>> {
    let dist_dir = target.join("distribution");
    fs::create_dir_all(&dist_dir)?;

    let policies_json = r#"{
  "policies": {
    "DisableTelemetry": true,
    "DisableFirefoxStudies": true,
    "DisablePocket": true,
    "DisableAppUpdate": true,
    "OverrideFirstRunPage": "",
    "OverridePostUpdatePage": ""
  }
}"#;

    fs::write(dist_dir.join("policies.json"), policies_json)?;
    Ok(())
}