APP_NAME = promocato
VERSION = 1.0.0
PYINSTALLER_FLAGS = --onefile --name $(APP_NAME) --windowed
DIST_DIR = dist

.PHONY: build-linux build-macos build-windows clean

build-linux:
	poetry run pyinstaller $(PYINSTALLER_FLAGS) app/main.py
	fpm -s dir -t deb -n $(APP_NAME) -v $(VERSION) --prefix /usr/local/bin $(DIST_DIR)/$(APP_NAME)=/usr/local/bin/$(APP_NAME)

build-macos:
	poetry run pyinstaller $(PYINSTALLER_FLAGS) app/main.py
	pkgbuild --identifier com.example.$(APP_NAME) \
	         --version $(VERSION) \
	         --install-location /usr/local/bin \
	         --component $(DIST_DIR)/$(APP_NAME) $(APP_NAME)-$(VERSION).pkg

build-windows:
	poetry run pyinstaller $(PYINSTALLER_FLAGS) app/main.py
	# Create NSIS installer if NSIS is installed
	if command -v makensis > /dev/null; then \
		echo "Generating NSIS installer..."; \
		makensis -V4 nsis-installer.nsi; \
	else \
		echo "NSIS not found. Skipping installer creation."; \
	fi

clean:
	rm -rf build $(DIST_DIR) *.spec *.deb *.pkg *.exe *.dmg *.msi
