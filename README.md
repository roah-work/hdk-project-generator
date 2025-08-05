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

## License

MIT License — See `LICENSE`.
