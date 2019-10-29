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

import buffer as bfr
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
        self._buffer_size = buffer_size
        self._current_file_index = 0
        self._read_index = 0
        self._buff = None

    ####################################################################################################################
    def begin_read(self) -> None:
        """
        A method to initialize read of image data into buffer.
        :return: None
        """
        self._allowable_files()
        self._buff = bfr.CircularBuffer(buffer_size=self._buffer_size)
        self._initialize_read()

    ####################################################################################################################
    def has_next(self) -> bool:
        """
        :return: True if another image available. False if not.
        """
        return self._current_file_index < self._num_files

    ####################################################################################################################
    def next_image(self) -> im.Image:
        """
        :return: next image object from file in list.
        """
        image = self._buff.get_data_at_index(self._current_file_index)

        # only read into the buffer if there is room for it
        if self._read_index < self._num_files:
            self._buff.forward(image=im.Image(file_name=self.acceptable_files[self._read_index]))
            self._read_index += 1

        self._current_file_index += 1

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
    def _initialize_read(self) -> None:
        """
        Read the first 'self._buffer_size' images from directory and store them in buffer.
        :return:
        """
        buffer_size = self._buffer_size
        num_files = self._num_files
        for ind in np.arange(np.min([buffer_size, num_files])):
            self._buff.forward(image=im.Image(file_name=self.acceptable_files[self._read_index]))
            self._read_index += 1

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

    import sys

    app = QApplication(sys.argv)

    
    dir_path = r'data/images'
    image_directory = ImageDirectory(path_directory=dir_path, buffer_size=4)
    image_directory.begin_read()
    w0 = im.Window(image_directory.next_image())
    w0.show()
    list_of_windows = []
    list_of_windows.append(w0)
    while image_directory.has_next() is True:

        w = im.Window(image_directory.next_image())
        w.show()
        list_of_windows.append(w)

    sys.exit(app.exec_())
