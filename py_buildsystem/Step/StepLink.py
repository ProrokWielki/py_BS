import os

from py_buildsystem.common import logger

from py_buildsystem.Step.Step import Step
from py_buildsystem.FilesFinder.FilesFinder import FilesFinder


class StepLink(Step):
    def __init__(self, step_config, step_name, linker):
        self.configuration = step_config
        self._check_config()

        self.linker = linker
        self.step_name = step_name

        self.files_finder = FilesFinder(list_of_paths_to_search=self. __source_directories)
        self.files_finder.set_files_extentions(self.__types)

    def _check_config(self):
        try:
            self.__source_directories = self.configuration["source_directories"]
        except KeyError:
            raise Exception("No source directories given")

        try:
            self.__output_file = self.configuration["output_file"]
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

    def get_type(self):
        return "link"

    def perform(self):
        self._create_output_directory()
        self._find_files()

        self.linker.link(self.__files_to_compile, self.__output_file, self.__additional_flags)

    def _find_files(self):
        self.__files_to_compile = self.files_finder.search()

    def _create_output_directory(self):
        os.makedirs(os.path.dirname(self.__output_file), exist_ok=True)
