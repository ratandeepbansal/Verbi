# App Icon

To add a custom icon to the Verbi app:

1. Create or obtain a `.icns` file (macOS app icon format)
2. Name it `icon.icns`
3. Place it in this `assets/` directory
4. Rebuild the app with PyInstaller

## Creating an .icns file:

### Option 1: Using iconutil (macOS)
```bash
# Create iconset directory
mkdir icon.iconset

# Add PNG images of various sizes:
# icon_16x16.png, icon_32x32.png, icon_64x64.png,
# icon_128x128.png, icon_256x256.png, icon_512x512.png, icon_1024x1024.png

# Convert to .icns
iconutil -c icns icon.iconset -o icon.icns
```

### Option 2: Using online tools
- https://cloudconvert.com/png-to-icns
- https://iconverticons.com/online/

### Option 3: Default icon
If no icon is provided, macOS will use the default Python app icon.

## Current Status
Currently using default icon. To add a custom icon, follow the steps above.
