# HDK Project Generator

A Python script to create and manage Houdini HDK SOP projects from a customizable template. It automates project setup, adds build steps to Visual Studio, and relaunches Houdini with the target `.hiplc` file on build.

---

## Features

- Copies a customizable `SOP_TEMPLATE/` folder to a specified HDK project directory.
- Replaces:
  - `TEMPLATE` → your project name
  - `<TEMPLATE>` → your project name
- Creates a `build/` subdirectory inside the generated project folder.
- Runs `cmake` to generate a Visual Studio solution.
- Adds build events to the `SOP_<ProjectName>.vcxproj`:
  - **Pre-build:** Kills the correct running Houdini instance using a `.pid` file.
  - **Post-build:** Relaunches Houdini with the corresponding `.hiplc` file.
- Stores the `.pid` file inside the generated project's `temp/` folder.
- Injects build events only into the `SOP_<ProjectName>.vcxproj`, not `ALL_BUILD` or others.

---

## Requirements

- Python 3.6+
- Houdini installed
- CMake (must be in system `PATH`)
- Environment variable `HFS` must be set  
  _Example (Windows CMD):_
  ```cmd
  setx HFS "D:\ProgramFiles\SideFx\Houdini20.0.751" /M
  ```
- Visual Studio with C++ build tools  
  _Default generator: `Visual Studio 17 2022`_

---

## Supported Platforms

- **Windows** (tested)
- **Linux/macOS** (template generation works; CMake generator and build event logic must be adapted manually)

---

## Usage Instructions

1. **Clone the repo anywhere you like**  
   Example:
   ```bash
   git clone https://github.com/roah-work/hdk-project-generator.git
   ```

2. **Ensure the template folder `SOP_TEMPLATE/` exists in the repo directory**  
   This must contain the base files like `.C`, `.h`, `CMakeLists.txt`, etc.

3. **Run the script**  
   ```bash
   python hdk_make_project.py -name=YourProjectName -project_dir="D:\Path\To\Your\HDKProjects" [-vs="Visual Studio 17 2022"]
   ```

   This will:
   - Create: `D:\Path\To\Your\HDKProjects\SOP_YourProjectName`
   - Replace all `TEMPLATE`/`<TEMPLATE>` in files and filenames
   - Create a `build/` subfolder and run `cmake` to generate `.sln`
   - Add pre-build and post-build event commands to the `.vcxproj`

---

## Arguments

- `-name` (**required**)  
  Your SOP project name. Replaces all placeholders.
  
- `-project_dir` (**required**)  
  Path to your **HDK projects root folder**. The script will create the project here.

- `-vs` (**optional**)  
  Visual Studio generator to use with CMake.  
  Default: `"Visual Studio 17 2022"`

---

## Folder Structure

```
# Repo Folder (can be cloned anywhere)
<repo_root>/
│
├── SOP_TEMPLATE/                # Your template SOP project
├── hdk_make_project.py          # Main project generator
├── hdk_hou_reload.py            # Relaunches Houdini and writes PID
├── hdk_hou_kill.py              # Kills previous Houdini using PID
└── ...

# Project Directory (specified via -project_dir)
<your_project_dir>/
└── SOP_<YourProjectName>/
    ├── SOP_<YourProjectName>.C
    ├── SOP_<YourProjectName>.h
    ├── CMakeLists.txt
    ├── build/                   # CMake output and VS solution
    ├── temp/                    # Stores SOP_<name>.pid
    └── Houdini_<Name>/          # Contains <name>.hiplc
```

---

## Notes

- The Houdini instance is tracked via a `.pid` file in the `temp/` subfolder.  
- On build:  
  - The **pre-build** event kills the old Houdini process.  
  - The **post-build** event launches Houdini and opens the `.hiplc` file.  
- To **debug**:  
  - Manually **attach the Visual Studio debugger** to the `houdini.exe` process after it launches via post-build.  
- The `.hiplc` file used can be replaced with any valid Houdini project file of your choice, including those with different license types you own.

---

## Pre and Post Build Events

This project uses **pre-build** and **post-build** events in the Visual Studio solution to automate managing the Houdini process when building your HDK node.

### What Are These Build Events?

- **Pre-build event**: This runs *before* the build starts. It kills any running Houdini instance associated with the current HDK project to ensure no locked files during build.
- **Post-build event**: This runs *after* a successful build. It launches Houdini and opens the specific `.hiplc` project file, reloading your newly built HDK node automatically.

### The Scripts Launched

- `hdk_hou_kill.py`: Reads a `.pid` file stored under the project’s `temp/` folder to find and terminate the running Houdini process.
- `hdk_hou_reload.py`: Launches Houdini with the specified `.hiplc` file and writes the new Houdini process ID to the `.pid` file in `temp/` for tracking.

### How to Modify or Disable These Events

The build events are configured in the Visual Studio `.vcxproj` file under the `<PostBuildEvent>` and `<PreBuildEvent>` sections.

- To **view or edit** the commands manually:
  1. Open the `.vcxproj` file corresponding to your SOP project.
  2. Locate the `<PreBuildEvent>` and `<PostBuildEvent>` XML nodes.
  3. Modify the command text to change the script paths, arguments, or remove the event entirely.

- To **enable or disable** events temporarily in Visual Studio:
  1. Right-click your project in Solution Explorer, select **Properties**.
  2. Under **Build Events**, modify or clear the **Pre-build event command line** or **Post-build event command line** fields.

- To **regenerate/restore** these events programmatically using the provided Python script:
  - Run the `add_build_events` function which injects the appropriate commands based on your project setup.

**Note:** Changing these settings affects the automatic Houdini reload workflow. Ensure your `.pid` file location and `.hiplc` path arguments remain consistent if modifying scripts or commands.

---


## License

MIT License — See `LICENSE`.
