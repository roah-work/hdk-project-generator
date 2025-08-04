import os
import shutil
import argparse
import sys
import subprocess
import xml.etree.ElementTree as ET

# === Parse argument ===
parser = argparse.ArgumentParser(description="Create HDK SOP node from template")
parser.add_argument("-name", help="Name to replace TEMPLATE with")
parser.add_argument("-vs", default="Visual Studio 17 2022", help="Visual Studio generator name for CMake")
args = parser.parse_args()

# === Enforce required argument ===
if not args.name:
    print("ERROR: You must specify -name=<HDK_Name>")
    sys.exit(1)

HDK_Name = args.name
vs_generator = args.vs
template_folder = "SOP_TEMPLATE"
new_folder = f"SOP_{HDK_Name}"

if not os.path.exists(template_folder):
    print(f"ERROR: '{template_folder}' does not exist.")
    sys.exit(1)

# === Copy folder ===
print(f"Copying '{template_folder}' to '{new_folder}'...")
shutil.copytree(template_folder, new_folder)

# === Create build folder ===
build_path = os.path.join(new_folder, "build")
os.makedirs(build_path, exist_ok=True)
print(f"Created: {build_path}")

# === Process files ===
for root, dirs, files in os.walk(new_folder, topdown=False):
    for filename in files:
        old_path = os.path.join(root, filename)

        # Replace content in applicable files
        if filename.endswith(('.txt', '.C', '.h')):
            with open(old_path, 'r', encoding='utf-8') as f:
                content = f.read()
            content = content.replace("<TEMPLATE>", HDK_Name)
            with open(old_path, 'w', encoding='utf-8') as f:
                f.write(content)

        # Rename files containing TEMPLATE
        if "TEMPLATE" in filename:
            new_filename = filename.replace("TEMPLATE", HDK_Name)
            new_path = os.path.join(root, new_filename)
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_filename}")

    # Rename folders containing TEMPLATE (only subdirectories)
    for dirname in dirs:
        if "TEMPLATE" in dirname:
            old_dir_path = os.path.join(root, dirname)
            new_dir_name = dirname.replace("TEMPLATE", HDK_Name)
            new_dir_path = os.path.join(root, new_dir_name)
            os.rename(old_dir_path, new_dir_path)
            print(f"Renamed folder: {dirname} -> {new_dir_name}")

# === Run CMake command ===
cmake_command = ['cmake', '..', '-G', vs_generator]

print(f"Running CMake command in: {build_path}")
result = subprocess.run(cmake_command, cwd=build_path, shell=True)

def set_compile_as_cpp(vcxproj_path):
    ET.register_namespace('', "http://schemas.microsoft.com/developer/msbuild/2003")
    tree = ET.parse(vcxproj_path)
    root = tree.getroot()
    ns = {'ns': "http://schemas.microsoft.com/developer/msbuild/2003"}

    changed = False
    for clcompile in root.findall('.//ns:ClCompile', ns):
        compile_as = clcompile.find('ns:CompileAs', ns)
        if compile_as is None:
            compile_as = ET.SubElement(clcompile, 'CompileAs')
            compile_as.text = "CompileAsCpp"
            changed = True
        elif compile_as.text != "CompileAsCpp":
            compile_as.text = "CompileAsCpp"
            changed = True

    if changed:
        tree.write(vcxproj_path, encoding='utf-8', xml_declaration=True)
        print(f"Updated {vcxproj_path} with CompileAsCpp")

if result.returncode != 0:
    print("CMake command failed.")
    sys.exit(1)
else:
    print("CMake command completed successfully.")
    # Post-process .vcxproj files
    for root, dirs, files in os.walk(build_path):
        for file in files:
            if file.endswith(".vcxproj"):
                set_compile_as_cpp(os.path.join(root, file))
