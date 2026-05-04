import os
import sys
import urllib.request
import subprocess
import shutil
import zipfile
import xml.etree.ElementTree as ET
import hashlib
from PIL import Image

APKTOOL_URL = "https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.9.3.jar"
SIGNER_URL = "https://github.com/patrickfav/uber-apk-signer/releases/download/v1.3.0/uber-apk-signer-1.3.0.jar"

APKTOOL_JAR = "apktool.jar"
SIGNER_JAR = "uber-apk-signer.jar"
BASE_APK = "kodi.apk"
DECOMPILED_DIR = "decompiled_kodi_new"
BACKUP_DIR = "Marmalade_Android_Final2_backup_202605031915"
CUSTOM_BUILD_DIR = "custom_build"

def download_file(url, filename):
    if not os.path.exists(filename):
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, filename)
        print("Download complete.")

def run_cmd(cmd):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"Error executing command. Exit code {result.returncode}")
        sys.exit(1)

def is_windows_only_addon(addon_path):
    """Check if an addon has only Windows .dll files and no Android .so files."""
    dll_count = sum(1 for _ in os.walk(addon_path) for f in _[2] if f.endswith('.dll'))
    so_count = sum(1 for _ in os.walk(addon_path) for f in _[2] if f.endswith('.so'))
    return dll_count > 0 and so_count == 0

def get_merged_addon_set(backup_addons, custom_addons):
    """Merge addons: backup is authoritative, custom_build supplements where backup is missing."""
    merged = set(backup_addons)
    for item in custom_addons:
        if item not in backup_addons and item != "service.skinsetter":
            merged.add(item)
    return sorted(merged)

def add_addon_to_zip(zf, addon_name, addon_path):
    """Add a single addon to the zip."""
    for root, dirs, files in os.walk(addon_path):
        for f in files:
            full = os.path.join(root, f)
            arcname = os.path.relpath(full, os.path.dirname(addon_path))
            zf.write(full, os.path.join("addons", arcname))

def update_icons(decompiled_dir, source_icon):
    """Resize and replace launcher icons in the decompiled APK."""
    if not os.path.exists(source_icon):
        print(f"WARNING: Source icon '{source_icon}' not found. Skipping icon update.")
        return

    sizes = {
        "drawable-ldpi": 36,
        "drawable-mdpi": 48,
        "drawable-hdpi": 72,
        "drawable-xhdpi": 96,
        "drawable-xxhdpi": 144,
        "drawable-xxxhdpi": 192,
    }
    img = Image.open(source_icon)
    res_dir = os.path.join(decompiled_dir, "res")
    for folder, size in sizes.items():
        dst = os.path.join(res_dir, folder, "ic_launcher.png")
        if os.path.exists(dst):
            resized = img.resize((size, size), Image.LANCZOS)
            resized.save(dst)
            print(f"  Updated {folder}/ic_launcher.png ({size}x{size})")
    print("  App icons updated successfully.")

def main():
    if not os.path.exists(BASE_APK):
        print(f"ERROR: '{BASE_APK}' not found.")
        sys.exit(1)

    print("--- Setting up Tools ---")
    download_file(APKTOOL_URL, APKTOOL_JAR)
    download_file(SIGNER_URL, SIGNER_JAR)

    print("\n--- Decompiling APK ---")
    if os.path.exists(DECOMPILED_DIR):
        shutil.rmtree(DECOMPILED_DIR)
    run_cmd(["java", "-jar", APKTOOL_JAR, "d", "-f", BASE_APK, "-o", DECOMPILED_DIR])

    print("\n--- Updating App Icons ---")
    update_icons(DECOMPILED_DIR, "icon.png")

    print("\n--- Preparing Custom Build (Extractor Method) ---")
    assets_dir = os.path.join(DECOMPILED_DIR, "assets")

    # Source addons from BOTH backup and custom_build (backup is primary)
    backup_addons_dir = os.path.join(BACKUP_DIR, "addons")
    custom_addons_dir = os.path.join(CUSTOM_BUILD_DIR, "addons")

    backup_addons = set()
    if os.path.exists(backup_addons_dir):
        backup_addons = set(os.listdir(backup_addons_dir))

    custom_addons = set()
    if os.path.exists(custom_addons_dir):
        custom_addons = set(os.listdir(custom_addons_dir))

    all_addons = get_merged_addon_set(backup_addons, custom_addons)

    print(f"Merged addon set: {len(all_addons)} addons (backup: {len(backup_addons)}, custom: {len(custom_addons)})")

    # Create custom_build.zip
    print("Creating custom_build.zip (ALL addons + userdata with guisettings.xml)...")
    zip_path = os.path.join(assets_dir, "custom_build.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add userdata from custom_build (includes guisettings.xml with skin.mimic.lr)
        userdata_dir = os.path.join(CUSTOM_BUILD_DIR, "userdata")
        if os.path.exists(userdata_dir):
            for root, dirs, files in os.walk(userdata_dir):
                for f in files:
                    full = os.path.join(root, f)
                    arcname = os.path.relpath(full, userdata_dir)
                    zf.write(full, os.path.join("userdata", arcname))
            print(f"  Added userdata from custom_build/")

        # Add merged addons
        for item in all_addons:
            # Try backup first, then custom_build
            addon_path = None
            if item in backup_addons:
                addon_path = os.path.join(backup_addons_dir, item)
            elif item in custom_addons:
                addon_path = os.path.join(custom_addons_dir, item)

            if not addon_path or not os.path.exists(addon_path):
                continue

            if os.path.isdir(addon_path) and is_windows_only_addon(addon_path):
                print(f"  Skipping Windows-only addon: {item}")
                continue

            add_addon_to_zip(zf, item, addon_path)

    print(f"  custom_build.zip created ({os.path.getsize(zip_path) / 1024 / 1024:.1f} MB)")

    # Generate build version hash from zip contents
    print("Generating build version...")
    with open(zip_path, 'rb') as f:
        build_hash = hashlib.md5(f.read()).hexdigest()[:12]
    version_file = os.path.join(assets_dir, "build_version.txt")
    with open(version_file, 'w') as f:
        f.write(build_hash)
    print(f"  Build version: {build_hash}")

    # Copy service.build.extractor to assets/addons/
    print("Injecting service.build.extractor into assets/addons/...")
    extractor_src = os.path.join(BACKUP_DIR, "addons", "service.build.extractor")
    if not os.path.exists(extractor_src):
        extractor_src = os.path.join(CUSTOM_BUILD_DIR, "addons", "service.build.extractor")

    if extractor_src and os.path.exists(extractor_src):
        extractor_dst = os.path.join(assets_dir, "addons", "service.build.extractor")
        if os.path.exists(extractor_dst):
            shutil.rmtree(extractor_dst)
        shutil.copytree(extractor_src, extractor_dst)
        print("  service.build.extractor injected")

    # Copy Open Code Player plugin directly into assets/addons/
    # and register in addon-manifest.xml for guaranteed availability
    opencode_src = os.path.join(CUSTOM_BUILD_DIR, "addons", "plugin.video.opencodeplayer")
    if os.path.exists(opencode_src):
        opencode_dst = os.path.join(assets_dir, "addons", "plugin.video.opencodeplayer")
        if os.path.exists(opencode_dst):
            shutil.rmtree(opencode_dst)
        shutil.copytree(opencode_src, opencode_dst)
        print("  plugin.video.opencodeplayer injected")

    manifest_path = os.path.join(assets_dir, "system", "addon-manifest.xml")
    tree = ET.parse(manifest_path)
    root = tree.getroot()
    existing = set(a.text for a in root.findall("addon"))
    
    for addon_id in ["service.build.extractor", "plugin.video.opencodeplayer"]:
        if addon_id not in existing:
            ET.SubElement(root, "addon").text = addon_id
            print(f"  Registered {addon_id} in addon-manifest.xml")
    
    tree.write(manifest_path, xml_declaration=False, encoding="unicode")

    print("\n--- Recompiling APK ---")
    unaligned_apk = "kodi_custom_unsigned.apk"
    run_cmd(["java", "-jar", APKTOOL_JAR, "b", DECOMPILED_DIR, "-o", unaligned_apk])

    print("\n--- Signing APK ---")
    run_cmd(["java", "-jar", SIGNER_JAR, "-a", unaligned_apk, "--allowResign"])

    print("\n==============================================")
    print("SUCCESS! APK ready:")
    print("kodi_custom_unsigned-aligned-debugSigned.apk")
    print("==============================================")

if __name__ == "__main__":
    main()
