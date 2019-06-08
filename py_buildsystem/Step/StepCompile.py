import os

from py_buildsystem.common import logger

from py_buildsystem.Step.Step import Step
from py_buildsystem.FilesFinder.FilesFinder import FilesFinder


class StepCompile(Step):

    def __init__(self, step_config, step_name, compiler):
        self.configuration = step_config
        self._check_config()

        self.compiler = compiler
        self.step_name = step_name

        self.files_finder = FilesFinder(list_of_paths_to_search=self. __source_directories, search_subdirectories=self.__search_subdirectories)
        self.files_finder.set_files_extentions(self.__types)

    def perform(self):
        self._create_outpu_directory()
        self._find_files()

        self.compiler.compile(self.__files_to_compile, self.__output_directory, self.__additional_flags)

    def get_type(self):
        return "compile"

    def _check_config(self):
        try:
            self.__source_directories = self.configuration["source_directories"]
        except KeyError:
            raise Exception("No source directories given")

        try:
            self.__output_directory = self.configuration["output_direcotry"]
        except KeyError:
            raise Exception("No output directory given")

        try:
            self.__types = self.configuration["types"]
        except KeyError:
            raise Exception("No type given")

        try:
            self.__additional_flags = self.configuration["additional_flags"]
        except KeyError:
            self.__additional_flags = []

        try:
            self.__search_subdirectories = self.configuration["search_subdirectories"]
        except KeyError:
            self.__search_subdirectories = True

    def _find_files(self):
        self.__files_to_compile = self.files_finder.search()

    def _create_outpu_directory(self):
        logger.debug("Creating " + self.__output_directory)
        os.makedirs(self.__output_directory, exist_ok=True)
