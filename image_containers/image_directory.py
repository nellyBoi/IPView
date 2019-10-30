"""
file: image_dir.py
author: Nelly Kane
date_originated: 10.24.2019

A module to read files from a dir and store their information in a buffer.

"""
import ntpath
import os
from os import listdir

import numpy as np
from PyQt5.QtWidgets import QApplication

import directorybuffer as bfr
from image_containers import image as im


########################################################################################################################
class ImageDirectory:
    ALLOWABLE_EXTENSIONS = ['.jpg', '.jpeg', '.JPG', '.png', '.PNG', '.tif', '.TIF']

    ####################################################################################################################
    def __init__(self, path_directory: str, buffer_size: int = 5):
        """
        :param path_directory:
        :param buffer_size: 
        """
        self._path_directory = path_directory
        # force odd buffer
        if buffer_size % 2 == 0:
            self._buffer_size = buffer_size - 1
        else:
            self._buffer_size = buffer_size

        self._current_file_index = -1
        self._read_index = -1
        self._buff = None
        self.acceptable_files = None
        self._num_files = None

        # used to control where the buff sits relative to the current image
        self.__middle_of_buffer_index = (self._buffer_size - 1) / 2

    ####################################################################################################################
    def begin_read(self) -> None:
        """
        A method to initialize read of image data into buffer.
        :return: None
        """
        self._allowable_files()
        self._buff = bfr.DirectoryBuffer(buffer_size=self._buffer_size)
        self._initialize_read()

    ####################################################################################################################
    def has_next(self) -> bool:
        """
        :return: True if the next image is available. False if not.
        """
        return self._current_file_index < self._num_files - 1

    ####################################################################################################################
    def forward(self) -> im.Image:
        """
        :return: next image object from file in list.
        """
        if not self.has_next():
            return None

        self._current_file_index += 1
        image = self._buff.get_data_at_index(self._current_file_index)

        # only read into the buffer if there is room for it
        if self.__middle_of_buffer_index < self._current_file_index < self._num_files - self.__middle_of_buffer_index:
            _read_index = int(self._current_file_index + self.__middle_of_buffer_index)
            self._buff.push_to_back(image=im.Image(file_name=self.acceptable_files[_read_index]))

        return image

    ####################################################################################################################
    def has_last(self) -> bool:
        """
        :return: True if the last image is available. False if not.
        """
        return self._current_file_index > 0

    ####################################################################################################################
    def backward(self) -> im.Image:
        """
        :return: last image object from file in list.
        """
        if not self.has_next():
            return None

        self._current_file_index -= 1

        image = self._buff.get_data_at_index(self._current_file_index)

        # only read into the buffer if there is room for it
        if self._current_file_index - 1 >= self.__middle_of_buffer_index:
            _read_index = int(self._current_file_index - self.__middle_of_buffer_index)
            self._buff.push_to_front(image=im.Image(file_name=self.acceptable_files[_read_index]))

        return image

    ####################################################################################################################
    def clear_memory(self) -> None:
        """
        A method to clear data from memory and reset read_index and current_file_index
        :return:
        """
        self._buff.clear()
        self._current_file_index = 0
        self._read_index = 0

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
    def _allowable_files(self) -> None:
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

        self.acceptable_files = acceptable_files
        self._num_files = len(self.acceptable_files)

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
    image_directory = ImageDirectory(path_directory=dir_path, buffer_size=4)
    image_directory.begin_read()
    list_of_windows = []

    if TEST_BACKWARDS:
        # image 1
        w = im.Window(image_directory.forward())
        w.show()
        list_of_windows.append(w)
        # image 2
        w = im.Window(image_directory.forward())
        w.show()
        list_of_windows.append(w)
        # image 3
        w = im.Window(image_directory.forward())
        w.show()
        list_of_windows.append(w)
        # image 4
        w = im.Window(image_directory.forward())
        w.show()
        list_of_windows.append(w)
        # image 3
        w = im.Window(image_directory.backward())
        w.show()
        list_of_windows.append(w)
        # image 2
        w = im.Window(image_directory.backward())
        w.show()
        list_of_windows.append(w)
        # image 1
        w = im.Window(image_directory.backward())
        w.show()
        list_of_windows.append(w)
    else:
        while image_directory.has_next() is True:

            w = im.Window(image_directory.forward())
            w.show()
            list_of_windows.append(w)

        sys.exit(app.exec_())
