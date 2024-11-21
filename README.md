# burn-build 🚀

<div align="center">  
  <p align="center">
    build system written in python for projects in C and C++
    <br />
    <a href="./docs/index.md"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#-getting-started">Getting Started</a>
    ·
    <a href="#-usage-examples">Basic Usage</a>
    ·
    <a href="https://github.com/alexeev-prog/burn-build/blob/main/LICENSE">License</a>
  </p>
</div>
<br>
<p align="center">
    <img src="https://img.shields.io/github/languages/top/alexeev-prog/burn-build?style=for-the-badge">
    <img src="https://img.shields.io/github/languages/count/alexeev-prog/burn-build?style=for-the-badge">
    <img src="https://img.shields.io/github/license/alexeev-prog/burn-build?style=for-the-badge">
    <img src="https://img.shields.io/github/stars/alexeev-prog/burn-build?style=for-the-badge">
    <img src="https://img.shields.io/github/issues/alexeev-prog/burn-build?style=for-the-badge">
    <img src="https://img.shields.io/github/last-commit/alexeev-prog/burn-build?style=for-the-badge">
</p>

## 🚀 Getting Started
burn-build is available on [PyPI](https://pypi.org/project/pyburn_build). Simply install the package into your project environment with PIP:

```bash
pip install pyburn_build
```

Once installed, you can start using the library in your Python projects.

## 💻 Usage Examples
Create project_config.json:

```json
{
    "metadata": {
        "name": "Example",
        "version": "0.1.0",
        "description": "Hello World app",
        "language": "cpp",
        "use_cmake": false,
        "cache_file": "cache.json",
        "features": ["pyechonext"]
    },

    "compiler": {
        "name": "g++",
        "base_compiler_flags": ["-Wall"]
    }
}
```

Create toolchain_config.json:

```json
{
    "prelude_commands": [],
    "targets": {
        "target1": {
            "compiler_options": ["-O2", "-pedantic"],
            "sources": ["src/main.c"],
            "output": "out/target1.out",
            "includes": [],
            "objects": [],
            "compiler": "gcc"
        },
        "target2": {
            "compiler_options": ["-O3", "-pedantic"],
            "sources": ["src/main2.cpp"],
            "output": "out/target2.out",
            "includes": [],
            "objects": []
        }
    },
    "post_commands": []
}
```

And create project:

```bash
python3 -m pyburn_build create --project-config example_configs/project_config.json --toolchain-config example_configs/toolchain_config.json
```

And build project:

```bash
python3 -m pyburn_build build --project-config example_configs/project_config.json --toolchain-config example_configs/toolchain_config.json
```

## Specification

### Project
Basic project information 

#### Metadata
Meta information and other general characteristics of the project.

 + name - project name
 + version - project version
 + description - short project description
 + language - main project language
 + use_cmake - use cmake flag (experimental)
 + cache_file - path to cache json file
 + features - list of enabled features (supported: pyechonext)

#### Compiler
Information about the compiler, basic flags.

 + name - main compiler name
 + base_compiler_flags - list of compiler flags

### Toolchain
Setting up tools, build chain, commands.

 + prelude_commands - Commands to execute before build
 + post_commands - Commands to execute after build
 + targets - dict with targets

#### Targets
Targets list

 + compiler_options - additional compiler flags
 + sources - list with sources for target
 + output - output filename
 + includes - include-files (C/C++)
 + objects - .o files
 + compiler - compiler command
