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
python -m py_buildsystem <project specific toolchain config> <project config> [path to the toolchain]
```

To use this buildsystem you have to provide two *yaml* files:

* project configuration, 
* project specific toolchain configuration.

If your toolchain is not in the *PATH* you have to provide its path to the buildystem.


### Project configuration


This file contains definitions of the steps to be peformed, compiler definitions and includes.

Available steps:

* compile,
* link. 

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

* source directories -- list of directiories in which the files to compile are located,
* output directory -- directory to which the output files will be writen,
* types -- file types to be compiled,
* search_subdirectories -- defines if the sub directories are searched (optional -- default = False).

#### Step link

Options available:

* source_directories -- list of directories where object files are located,
* output_file -- executable file which will be created after linking,
* types -- file types to be linked.

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
* arm-none-eabi -- GCC_ARM,
* gcc -- GCC.

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

