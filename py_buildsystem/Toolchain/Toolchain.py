import os
import sys
import yaml
import subprocess

from .Linker.Linker import Linker
from .Compiler.Compiler import Compiler

from ConfigReader.ConfigReader import ConfigReader

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))


path_to_configs = os.path.dirname(__file__).replace("\\", "/") + "/ToolchainsConfigs"


class Toolchain(ConfigReader):
    def __init__(self, config_yaml_file, path_to_toolchain=""):

        ConfigReader.__init__(self, config_yaml_file)

        self._check_compiler_config_file()

        self.__linker_path = os.path.join(path_to_toolchain, self.__linker_name).replace("\\", "/")
        self.__compiler_path = os.path.join(path_to_toolchain, self.__compiler_name).replace("\\", "/")

        self._check_toolchain_path()

        self.__compiler = Compiler(self.__compiler_path, self.__define_flag, self.__output_flag,
                                   self.__compile_flag, self.__include_flag)

        self.__compiler.set_flags(self.__compiler_flags)

        self.__linker = Linker(self.__linker_path, self.__output_flag, self.__command_line_file)
        self.__linker.set_flags(self.__linker_flags)

    def get_compiler(self):
        return self.__compiler

    def get_linker(self):
        return self.__linker

    def _check_config(self):
        try:
            self.__choosen_compiler = self.configuration["compiler"]
        except KeyError:
            raise Exception("You must provide compiler name in a compiler configuration file")

        try:
            self.__compiler_flags = self.configuration["compiler_flags"]
        except KeyError:
            self.__compiler_flags = []

        try:
            self.__linker_flags = self.configuration["linker_flags"]
        except KeyError:
            self.__linker_flags = []

    def _check_compiler_config_file(self):
        try:
            with open(os.path.join(path_to_configs, self.__choosen_compiler + ".yaml").replace("\\", "/"), "r") as compiler_config_file:
                compiler_config = yaml.load(compiler_config_file)

        except FileNotFoundError:
            raise Exception("Configuration file for the compiler was not found.")

        self.__compiler_name = compiler_config["compiler"]
        self.__linker_name = compiler_config["linker"]

        self.__define_flag = compiler_config["define_flag"]
        self.__output_flag = compiler_config["output_flag"]
        self.__compile_flag = compiler_config["compile_flag"]
        self.__include_flag = compiler_config["include_flag"]
        self.__version_flag = compiler_config["version_flag"]
        self.__command_line_file = compiler_config["comand_line_file"]

    def _check_toolchain_path(self):
        try:
            subprocess.check_output([self.__linker_path, self.__version_flag])
            subprocess.check_output([self.__compiler_path, self.__version_flag])
        except FileNotFoundError:
            raise Exception("Can not find the compilers executable, check if the compilers path is correct or if the compiler is in a PATH.")
