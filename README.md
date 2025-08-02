# HDK Project Generator

A Python script to create customizable Houdini HDK SOP projects from a template folder. It automates folder copying, filename and content replacement, and sets up a CMake build directory with Visual Studio project generation.

---

## Features

- Copies a predefined `SOP_TEMPLATE` folder to a new project folder.
- Replaces placeholders in filenames and file contents:
  - `TEMPLATE` → your project name
  - `<TEMPLATE>` → your project name
- Creates a `build` directory inside the new project folder.
- Runs `cmake` to generate a Visual Studio solution (or any CMake-compatible generator).
- CLI interface using `-name` and `-vs` options.

---

## Note
- This is a copy of the SOP_Star default example template provided by SideFx, and hence when compiled by default will retain the SOP_Star parameters and functionality. 
- Please modify the project files post generation to fit your project needs. 



## Requirements

- Python 3.6 or higher
- CMake (must be accessible from system PATH)
- Houdini installed
- Environment variable `HFS` must be set and point to the Houdini installation folder  
  _Example on Windows CMD:_  
  ```cmd
  setx HFS "D:\ProgramFiles\SideFx\Houdini20.0.751" /M
  ```
- Visual Studio (Windows only), with C++ build tools installed  
  _Default generator used: `Visual Studio 17 2022`_

---

## Supported Platforms

- **Windows** (primary, tested with Visual Studio generators)
- **Linux/macOS** (template generation will work; you must adjust the generator accordingly)

---

## Usage Instructions

1. **Clone the repository into your desired project location, or to a local folder of choice.**  
   ```bash
   git clone https://github.com/roah-work/hdk-project-generator.git
   ```

2. **Ensure `SOP_TEMPLATE/` folder is present**  
   This folder must exist in the repo and contains the base files to duplicate and rename.

3. **Run the script**  
   ```bash
   python hdk_make_project.py -name=YourProjectName [-vs="Visual Studio 17 2022"]
   ```

---

### Arguments:

- `-name` (**required**)  
  The name that replaces all `TEMPLATE` and `<TEMPLATE>` occurrences in file names and contents.

- `-vs` (**optional**)  
  The Visual Studio generator string to pass to `cmake -G`.  
  Default: `"Visual Studio 17 2022"`

---

## Example

```bash
python hdk_make_project.py -name=MyCustomNode -vs="Visual Studio 17 2022"
```

This will:
- Create a new folder `SOP_MyCustomNode`
- Replace all `TEMPLATE` references in file names and contents
- Create a `build/` subfolder
- Run `cmake .. -G "Visual Studio 17 2022"` inside the build folder

---

## Folder Structure

```
/your/project/root/
│
├── SOP_TEMPLATE/              # Your HDK project template folder
│   ├── SOP_TEMPLATE.C
│   ├── SOP_TEMPLATE.h
│   ├── hdk_TEMPLATE.txt
│   ├── CMakeLists.txt
│   └── ...
│
├── hdk_make_project.py        # This script
├── LICENSE                    # MIT License
│
└── SOP_<YourProjectName>/     # Generated result
    ├── SOP_<YourProjectName>.C
    ├── SOP_<YourProjectName>.h
    ├── ...
    └── build/                 # CMake build directory
```

---

## License

This project is licensed under the [MIT License](LICENSE).
