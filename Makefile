# Makefile

# Paths
ASCEND_INSTALLER_DIR := ascen-installer
ASCEND_CORE_DIR := ascend-core
PROFILE_DIR := ascend-profile

# Targets
all: install-binary bundle

install-binary:
	@echo "Building Ascend Installer"
	cargo build --release -p $(ASCEND_INSTALLER_DIR)

bundle:
	@echo "Bundling final distribution..."
	tar czf ascend-browser.tar.gz $(ASCEND_INSTALLER_DIR)/target/release/$(ASCEND_INSTALLER_DIR) $(ASCEND_CORE_DIR)/target/release/$(ASCEND_CORE_DIR) $(PROFILE_DIR)/src/main.rs

clean:
	rm -rf $(ASCEND_INSTALLER_DIR)/target $(ASCEND_CORE_DIR)/target $(PROFILE_DIR)/src main.exe ascend-browser.tar.gz
