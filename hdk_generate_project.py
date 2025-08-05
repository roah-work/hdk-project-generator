import os
import shutil
import argparse
import sys
import subprocess
import xml.etree.ElementTree as ET

# === Parse argument ===
parser = argparse.ArgumentParser(description="Create HDK SOP node from template")
parser.add_argument("-name", required=True, help="Name to replace TEMPLATE with")
parser.add_argument("-vs", default="Visual Studio 17 2022", help="Visual Studio generator name for CMake")
parser.add_argument("-project_dir", required=True, help="Destination folder for the new HDK project")
args = parser.parse_args()

HDK_Name = args.name
vs_generator = args.vs
project_dir = os.path.abspath(args.project_dir)

template_folder = "SOP_TEMPLATE"
new_folder = os.path.join(project_dir, f"SOP_{HDK_Name}")

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

    # Rename folders containing TEMPLATE
    for dirname in dirs:
        if "TEMPLATE" in dirname:
            old_dir_path = os.path.join(root, dirname)
            new_dir_name = dirname.replace("TEMPLATE", HDK_Name)
            new_dir_path = os.path.join(root, new_dir_name)
            os.rename(old_dir_path, new_dir_path)
            print(f"Renamed folder: {dirname} -> {new_dir_name}")

# === Run CMake ===
cmake_command = ['cmake', '..', '-G', vs_generator]
print(f"Running CMake command in: {build_path}")
result = subprocess.run(cmake_command, cwd=build_path, shell=True)

def add_build_events(vcxproj_path, hdk_name, project_dir):
    ET.register_namespace('', "http://schemas.microsoft.com/developer/msbuild/2003")
    ns = "http://schemas.microsoft.com/developer/msbuild/2003"
    nsmap = {'ns': ns}

    tree = ET.parse(vcxproj_path)
    root = tree.getroot()

    for item_group in root.findall('ns:ItemDefinitionGroup', nsmap):
        cond = item_group.attrib.get('Condition', '')
        if "'Debug|x64'" in cond:
            # PreBuildEvent
            prebuild = item_group.find('ns:PreBuildEvent', nsmap)
            if prebuild is None:
                prebuild = ET.SubElement(item_group, f'{{{ns}}}PreBuildEvent')

            pre_command = prebuild.find('ns:Command', nsmap)
            if pre_command is None:
                pre_command = ET.SubElement(prebuild, f'{{{ns}}}Command')

            # PostBuildEvent
            postbuild = item_group.find('ns:PostBuildEvent', nsmap)
            if postbuild is None:
                postbuild = ET.SubElement(item_group, f'{{{ns}}}PostBuildEvent')

            post_command = postbuild.find('ns:Command', nsmap)
            if post_command is None:
                post_command = ET.SubElement(postbuild, f'{{{ns}}}Command')

            script_dir = os.path.dirname(os.path.abspath(__file__))

            hiplc_file = os.path.join(project_dir, f"SOP_{hdk_name}", f"Houdini_{hdk_name}", f"{hdk_name}.hiplc")

            kill_script = os.path.join(script_dir, 'hdk_hou_kill.py')
            launch_script = os.path.join(script_dir, 'hdk_hou_launch.py')

            pre_command.text = f'python "{kill_script}" -file "{hiplc_file}"'
            post_command.text = f'python "{launch_script}" -file "{hiplc_file}"'

            break

    tree.write(vcxproj_path, encoding='utf-8', xml_declaration=True)
    print(f"Build events injected into {vcxproj_path}")


def set_compile_as_cpp(vcxproj_path):
    ET.register_namespace('', "http://schemas.microsoft.com/developer/msbuild/2003")
    tree = ET.parse(vcxproj_path)
    root = tree.getroot()
    ns = {'ns': "http://schemas.microsoft.com/developer/msbuild/2003"}

    for item_group in root.findall("ns:ItemDefinitionGroup", ns):
        condition = item_group.attrib.get("Condition", "")
        if "'Debug|x64'" in condition:
            cl_compile = item_group.find("ns:ClCompile", ns)
            if cl_compile is not None:
                additional_options = cl_compile.find("ns:AdditionalOptions", ns)
                if additional_options is None:
                    additional_options = ET.SubElement(cl_compile, f'{{{ns["ns"]}}}AdditionalOptions')
                    additional_options.text = "%(AdditionalOptions) /TP"
                elif "/TP" not in additional_options.text:
                    additional_options.text += " /TP"
            break

    tree.write(vcxproj_path, encoding='utf-8', xml_declaration=True)
    print(f"Updated {vcxproj_path} with /TP in AdditionalOptions")

# === Post-process VCXPROJ ===
if result.returncode != 0:
    print("CMake command failed.")
    sys.exit(1)
else:
    print("CMake command completed successfully.")
    target_vcxproj = f"SOP_{HDK_Name}.vcxproj"
    for root, dirs, files in os.walk(build_path):
        for file in files:
            if file == target_vcxproj:
                full_path = os.path.join(root, file)
                set_compile_as_cpp(full_path)
                add_build_events(full_path, HDK_Name, project_dir)

