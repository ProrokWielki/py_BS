# py_buildsysten

py_buildsystem is a python based buildsystem. It is configured using *yaml* files.

## Instalation

The py_buildsytem can be installed using pip, or it can be installed from the source code.

### from pip

```
pip install py_buildsystem
```

### from source code

```
git clone https://github.com/ProrokWielki/py_buildsystem.git
cd py_buildsystem
python setup.py install
```


## Usage

To run the package use this command:

```
usage: py_buildsystem [-h] [-v] -pcc PROJECT_COMPILER_CONFIG -pc PROJECT_CONFIG [compiler path]
```

Options:

```
positional arguments:
  compiler path         Path to compiler

optional arguments:
  -h, --help            show this help message and exit
  -pcc PROJECT_COMPILER_CONFIG, --project_compiler_config PROJECT_COMPILER_CONFIG
                        Project specific toolchain configuration file
  -pc PROJECT_CONFIG, --project_config PROJECT_CONFIG
                        Project configuration file
  -v, --verbose         verbose mode
```

To use this buildsystem you have to provide two *yaml* files:

* project configuration, 
* project specific toolchain configuration.

If your toolchain is not in the *PATH* you have to provide its path to the toolchain


### Project configuration


This file contains definitions of the steps to be peformed, compiler definitions and includes.

Available steps:

* compile,
* link,
* git,
* command. 

Project configuration file example:

```
defines:
  - STM32L452xx

includes:
  - ../../LIB/CMSIS/Device/ST/STM32L4xx/Include
  - ../../LIB/CMSIS/Include

steps:
  - compile MCU:
    source_directories: 
      - ../../MCU

    output_direcotry: ../../Output/Obj/MCU

    types:
      - .c
      - .s

  - link Everything:
    source_directories:
      -  ../../Output/Obj

    output_file: ../../Output/file.elf

    types:
      - .o
```


#### Step compile

Options available:

* source directories -- list of directories in which the files to compile are located,
* output directory -- directory to which the output files will be written,
* types -- file types to be compiled,
* search_subdirectories -- defines if the sub directories are searched (optional -- default = False).
* additional_flags -- list of additional flags for this step (optional)

#### Step link

Options available:

* source_directories -- list of directories where object files are located,
* output_file -- executable file which will be created after linking,
* types -- file types to be linked.
* additional_flags -- list of additional flags for this step (optional)

#### Step git

Options available:

* repo_location -- location of the repository
* destination -- repository clone destination
* branch --  branch to clone (optional -- default = master)

#### Step command

Options available:

* location -- location from where to perform commands
* commands -- list of commands to call

### Project specific toolchain configuration

This file defines three thinks:

* toolchain to be used,
* compilator flags,
* linker flags.

Project specific toolchain configuration file example:

```
compiler: GCC_ARM

compiler_flags:
  - -mcpu=cortex-m4

linker_flags:
  - --specs=nosys.specs
  - -T ../../MCU/STM32L452RETx_FLASH.ld
```

### Toolchain configuration

Every toolchain has to have its configuration file. The file contains basic inforamtion about the toolchain, executables names and defines basic flags used by the toolchain. 

Currently supported toolchains:
* arm-none-eabi-gcc -- GCC_ARM,
* arm-none-eabi-g++ -- G++_ARM,
* gcc -- GCC.
* g++ -- G++

If the toolchain you wish to use is not supported you can add the configuration file to the project.

Toolchain configuration file example:

```
compiler: arm-none-eabi-gcc
linker:   arm-none-eabi-gcc

define_flag:  -D
output_flag:  -o
compile_flag: -c
include_flag: -I
comand_line_file: "-Wl,@"
version_flag: --version
```

