build:
	cargo build --release
	mkdir -p dist
	cp target/release/ascend-core.exe dist/ascend.exe
	cp target/release/ascend-installer.exe dist/ascend-installer.exe

clean:
	cargo clean
	rm -rf dist