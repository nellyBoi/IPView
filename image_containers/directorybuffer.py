"""
file: directorybuffer.py
author: Nelly Kane
date_originated: 10.29.2019

A circular buffer to hold Image objects and image/directory data from a given image directory.

"""
import ntpath
import os
import sys
from enum import Enum

import numpy as np

from image_containers import image as im


########################################################################################################################
class Direction(Enum):
    """
    Enum to hold travel direction of directory read
    """
    FORWARDS = 1
    BACKWARDS = 2


########################################################################################################################
class DirectoryBuffer:
    """
    Class to store buffer_size im.Image objects created externally from a provided directory.
    HOW IT WORKS:
        - Buffer construction will read the first 'buffer_size' compatible files into the buffer.
        - read_index will begin at -1. As next file is read 'read_index' will increment by 1 and read a new image. If
        the last is called for read, 'read_index' will decrement by 1.
        -  buffer_index for  creating new im.Image objects will occur internally, replacing objects in the buffer in
        a circular manner.
        - current object being read will exist in the 'middle' of the buffer from a directory position point of view,
        although it is important to note this is not necessarily the center buffer element since objects will be
        replaced in a circular fashion.
    """

    ####################################################################################################################
    def __init__(self, directory: str, compatible_files: list, buffer_size: int = 5):
        """

        :param directory:
        :param compatible_files:
        :param buffer_size:
        """
        self.__directory = directory
        self.__compatible_files = compatible_files
        self.__num_files = len(compatible_files)

        # force buffer size to be odd
        if buffer_size % 2 == 0:
            self.__buffer_size = buffer_size - 1
            print('WARNING: Buffer size must be odd, using size: ', + str(self.__buffer_size))
        else:
            self.__buffer_size = buffer_size

        # instantiating buffer data
        self.__data = [None] * buffer_size

        # middle index of buffer
        self.__middle_of_buffer = int((self.__buffer_size - 1) / 2)

        # index creation. buffer indices will pertain to buffer's circular order, file_list indices pertain to indices
        # of compatible_files.
        self.__buffer_read_idx = None
        self.__buffer_replace_idx = None
        self.__file_list_read_idx = None
        self.__file_list_replace_idx = None
        self.__read_direction = None  # used for controlling indices during a direction change
        self.__reset_all_indices()

        self.__initialize_read()

    ####################################################################################################################
    def next_image(self) -> im.Image:
        """
        Method to return the next image object in list of compatible files.
        :return: im.Image object
        """
        self.__increment_buffer_read_idx()
        this_image = self.__data[self.__buffer_read_idx]

        self.__file_list_read_idx += 1

        # replace object in buffer only if conditions are met
        if self.__file_list_read_idx > self.__middle_of_buffer and self.__file_list_replace_idx < (
                self.__num_files - 1):
            self.__file_list_replace_idx += 1

            if self.__read_direction == Direction.FORWARDS:
                self.__increment_buffer_replace_idx()

            self.__read_direction = Direction.FORWARDS
            self.__push_to_back()

        return this_image

    ####################################################################################################################
    def previous_image(self) -> im.Image:
        """
        Method to return the next image object in list of compatible files.
        :return: im.Image object
        """
        self.__decrement_buffer_read_idx()
        this_image = self.__data[self.__buffer_read_idx]

        self.__file_list_read_idx -= 1

        # replace object in buffer only if conditions are met
        if self.__file_list_read_idx > (self.__middle_of_buffer - 1):
            self.__file_list_replace_idx -= 1

            if self.__read_direction == Direction.BACKWARDS:
                self.__decrement_buffer_replace_idx()

            self.__read_direction = Direction.BACKWARDS
            self.__push_to_front()

        return this_image

    ####################################################################################################################
    def has_next(self) -> bool:
        """
        :return: true if another file available, false if not
        """
        return (self.__file_list_read_idx + 1) < self.__num_files

    ####################################################################################################################
    def has_previous(self) -> bool:
        """
        :return: true if previous file available, false if not
        """
        return (self.__file_list_read_idx - 1) >= 0

    ####################################################################################################################
    def clear(self) -> None:
        """
        Method to clear the buffer.
        """
        self.__data = [None] * self.__buffer_size
        self.__reset_all_indices()

        return

    ####################################################################################################################
    def __initialize_read(self) -> None:
        """
        Read the first 'self.__buffer_size' images from directory and store them in buffer.
        """
        self.__read_direction = Direction.FORWARDS
        for idx in np.arange(np.min([self.__buffer_size, self.__num_files])):
            self.__file_list_replace_idx += 1
            self.__increment_buffer_replace_idx()
            self.__push_to_back()

    ####################################################################################################################
    def __push_to_back(self) -> None:
        """
        Note: the '__file_list_replace_idx' remains at the bottom of the directory structure and has been decremented
        but the actual file to create and object with is above it by '__buffer_size' positions.
        """
        filename = os.path.join(self.__directory, self.__compatible_files[self.__file_list_replace_idx])
        self.__data[self.__buffer_replace_idx] = im.Image(file_name=filename)

        return

    ####################################################################################################################
    def __push_to_front(self) -> None:
        """
        Method to push to the front of buffer
        :param image: instance of Image
        """
        filename = os.path.join(self.__directory,
                                self.__compatible_files[self.__file_list_replace_idx - self.__buffer_size + 1])
        self.__data[self.__buffer_replace_idx] = im.Image(file_name=filename)

        return

    ####################################################################################################################
    def __increment_buffer_read_idx(self) -> None:
        """
        Increment index with circular method. For instance, if the buffer_size is 5, the order of the index upon
        incrementation would be [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, ...].
        """
        self.__buffer_read_idx = (self.__buffer_read_idx + 1) % self.__buffer_size
        return

    ####################################################################################################################
    def __decrement_buffer_read_idx(self) -> None:
        """
        Decrement the buffer to read in the reverse order.
        """
        self.__buffer_read_idx = (self.__buffer_read_idx + self.__buffer_size - 1) % self.__buffer_size
        return

    ####################################################################################################################
    def __increment_buffer_replace_idx(self) -> None:
        """
        Increment index with circular method. For instance, if the buffer_size is 5, the order of the index upon
        incrementation would be [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, ...].
        """
        self.__buffer_replace_idx = (self.__buffer_replace_idx + 1) % self.__buffer_size
        return

    ####################################################################################################################
    def __decrement_buffer_replace_idx(self) -> None:
        """
        Decrement the buffer to read in the reverse order.
        """
        self.__buffer_replace_idx = (self.__buffer_replace_idx + self.__buffer_size - 1) % self.__buffer_size
        return

    ####################################################################################################################
    def __reset_all_indices(self) -> None:
        """
        Reset all indices
        """
        self.__buffer_read_idx = -1
        self.__buffer_replace_idx = -1
        self.__file_list_read_idx = -1
        self.__file_list_replace_idx = -1
        self.__read_direction = 0

        return


########################################################################################################################
if __name__ == '__main__':

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    dir_path = r'data/images'

    # get list of files
    files_name_only = []
    for file in os.listdir(dir_path):
        files_name_only.append(ntpath.basename(file))

    directory_buffer = DirectoryBuffer(directory=dir_path, compatible_files=files_name_only, buffer_size=3)

    list_of_windows = []
    while directory_buffer.has_next():  # test forwards
        image = directory_buffer.next_image()
        w = im.Window(image=image)
        w.show()
        list_of_windows.append(w)
    while directory_buffer.has_previous():  # test backwards
        image = directory_buffer.previous_image()
        w = im.Window(image=image)
        w.show()
        list_of_windows.append(w)

    # show one more forwards
    image = directory_buffer.next_image()
    w = im.Window(image=image)
    w.show()
    list_of_windows.append(w)
    image = directory_buffer.next_image()
    w = im.Window(image=image)
    w.show()
    list_of_windows.append(w)

    sys.exit(app.exec_())
