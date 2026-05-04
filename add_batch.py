import xml.etree.ElementTree as ET
import sys
import os

batch_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

from addon_batches import addons_batch1, addons_batch2, addons_batch3, addons_batch4

batches = {1: addons_batch1, 2: addons_batch2, 3: addons_batch3, 4: addons_batch4}

addons_to_add = batches[batch_num]

manifest_path = 'decompiled_clean/assets/system/addon-manifest.xml'
tree = ET.parse(manifest_path)
root = tree.getroot()
existing = set(a.text for a in root.findall('addon'))

print(f"Adding batch {batch_num} ({len(addons_to_add)} addons)...")
for addon in addons_to_add:
    if addon not in existing:
        addon_dir = os.path.join('custom_build/addons', addon)
        if os.path.exists(addon_dir):
            import shutil
            src = addon_dir
            dst = os.path.join('decompiled_clean/assets/addons', addon)
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            ET.SubElement(root, 'addon').text = addon
            print(f"  Added {addon}")
        else:
            print(f"  Skipped {addon} (not found in custom_build)")
    else:
        print(f"  Already exists: {addon}")

tree.write(manifest_path, xml_declaration=False, encoding='unicode')
print(f"Batch {batch_num} added to addon-manifest.xml")
