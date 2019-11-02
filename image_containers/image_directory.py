"""
file: image_directory.py
author: Nelly Kane
date_originated: 10.24.2019

"""
import ntpath
import os
from os import listdir

from PyQt5.QtWidgets import QApplication

import directorybuffer as bfr
from image_containers import image as im


########################################################################################################################
class ImageDirectory:
    """
    Class to iterate through a directory both forwards and backwards while skipping files that are incompatible. Images
    are stored in a buffer.
    """
    ALLOWABLE_EXTENSIONS = ['.jpg', '.jpeg', '.JPG', '.png', '.PNG', '.tif', '.TIF']

    ####################################################################################################################
    def __init__(self, path_directory: str, buffer_size: int = 5):
        """
        :param path_directory:
        :param buffer_size: 
        """
        self._path_directory = path_directory
        self._buffer_size = buffer_size
        self._buffer = None
        self.__acceptable_files = None
        self._num_acceptable_files = None

    ####################################################################################################################
    def begin_read(self) -> None:
        """
        A method to initialize read of image data into buffer.
        :return: None
        """
        self.__allowable_files()
        self._buffer = bfr.DirectoryBuffer(directory=self.__path_directory, compatible_files=self.__acceptable_files,
                                           buffer_size=self._buffer_size)
        self._initialize_read()

    ####################################################################################################################
    def forward(self) -> im.Image:
        """
        :return: next image object from file in list.
        """
        if self._buffer.has_next():
            return self._buffer.next_image()

        return None

    ####################################################################################################################
    def backward(self) -> im.Image:
        """
        :return: last image object from file in list if it exists
        """
        if self._buffer.has_last():
            return self._buffer.last_image()

        return None

    ####################################################################################################################
    def clear_memory(self) -> None:
        """
        A method to clear data from memory.
        :return:
        """
        self._buffer.clear()

        return

    ####################################################################################################################
    def get_list_of_allowable_files(self) -> list:
        """
        :return: a list of all allowable files without full path
        """
        files_name_only = []
        for file in self.acceptable_files:
            files_name_only.append(ntpath.basename(file))

        return files_name_only

    ####################################################################################################################
    def __allowable_files(self) -> None:
        """
        A method to store files only with extensions defined in ALLOWABLE_EXTENSIONS in a list.
        :return: self.acceptable_files, self_num_files
        """
        all_files = ImageDirectory.list_all_files(path_dir=self._path_directory)

        acceptable_files = []
        for file in all_files:
            file_ext = os.path.splitext(file)[-1]
            if file_ext in ImageDirectory.ALLOWABLE_EXTENSIONS:
                acceptable_files.append(file)

        self.__acceptable_files = acceptable_files
        self._num_acceptable_files = len(self.acceptable_files)

        return

    ####################################################################################################################
    @staticmethod
    def list_all_files(path_dir: str) -> list:
        """
        :param path_dir: path to dir
        :return: list of files in dir
        """
        return [os.path.join(path_dir, f) for f in listdir(path_dir) if os.path.isfile(os.path.join(path_dir, f))]


########################################################################################################################
if __name__ == '__main__':

    TEST_BACKWARDS = True

    import sys

    app = QApplication(sys.argv)

    dir_path = r'data/images'
    image_directory = ImageDirectory(path_directory=dir_path, buffer_size=3)
    image_directory.begin_read()
    list_of_windows = []

