build:
	cargo build --release
	mkdir -p dist
	cp target/release/ascend-core dist/ascend.exe
	cp target/release/ascend-installer dist/ascend-installer.exe

clean:
	cargo clean
	rm -rf dist