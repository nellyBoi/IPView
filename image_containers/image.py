"""
:file: image.py
:author: Nelly Kane
:date_originated: 10.23.2019
:modifications: 12.07.2019

A module for holding, accessing and manipulating image data.
"""
import ReadFRED as fred

import ntpath
from enum import Enum

import cv2
import matplotlib.pyplot as plt
import numpy as np

import os.path


########################################################################################################################
class NotImplementedException(BaseException):
    """
    Exception raised when a file-read was executed and the conversion to a QImage object is not possible due to an
    unimplemented file-type.
    """
    pass


########################################################################################################################
class ImageFormat(Enum):
    """
    An enum to hold image types compatible with Image class.
    """
    RGB = 1
    ARGB = 2  # TODO how do we know if its this or RGBA?
    GRAY = 3
    RGBA = 4


########################################################################################################################
class ImageDataType(Enum):
    """
    An enum to hold image data types compatible with Image class.
    """
    UINT8 = 1  # Unsigned integer (0 to 255)
    UINT16 = 2  # Unsigned integer (0 to 65535)


########################################################################################################################
class Image:
    """
    Class to hold image from a file or from a compatible numpy array.
    """

    ####################################################################################################################
    def __init__(self, array: np.ndarray = None, path: str = None, file_name: str = None):
        """
        :param array: numpy nd array
        :param path: full path to file folder
        :param file_name: name of image file
        """
        if array is not None:
            self.__array = array
            self.__name = 'from_array'

        else:
            if path is not None:
                file_name = path + file_name

            # if image is .dat file use the FRED image reader.
            extension = os.path.splitext(file_name)[1]
            if extension == '.dat':
                self.__array = fred.read(filename=file_name)
            else:
                self.__array = plt.imread(file_name, cv2.IMREAD_UNCHANGED).copy()

            self.__name = ntpath.basename(file_name)

        self.__array_dimensions = len(self.__array.shape)
        self.__image_format = None
        if self.__array_dimensions == 2:
            self.__image_format = ImageFormat.GRAY
        elif self.__array_dimensions == 3:
            if self.__array.shape[2] == 3:
                self.__image_format = ImageFormat.RGB
            elif self.__array.shape[2] == 4:
                self.__image_format = ImageFormat.RGBA

        self.__image_data_type = None
        self.__set_data_type()

        if self.__image_format is None:
            raise NotImplementedException

        if self.__image_data_type is None:
            raise NotImplementedException

    ####################################################################################################################
    def get_name(self) -> str:
        """
        :return: file name
        """
        return self.__name

    ####################################################################################################################
    def get_array(self) -> np.ndarray:
        """
        :return: Original numpy array.
        NOTE: This is the original, often needed to compute on image (i.e. increasing contrast since operating on
        already processed image may have undesired accumulations.
        """
        return self.__array

    ####################################################################################################################
    def get_format(self) -> str:
        """
        :return: Image format
        """
        return self.__image_format.name

    ####################################################################################################################
    def get_data_type(self) -> str:
        """
        :return: Image data-type
        """
        return self.__image_data_type.name

    ####################################################################################################################
    def get_dimensions(self) -> int:
        """
        :return: dimensions of underlying array; 2 if gray, 3 if color.
        """
        return self.__array_dimensions

    ####################################################################################################################
    def get_pixel(self, row: int, col: int) -> np.ndarray:
        """
        :param row: row value of pixel
        :param col: column value of pixel
        :return: All channels of pixel.
        NOTE: It is the responsibility of the user on the call side to know the ImageFormat.
        """
        if self.__array_dimensions == 2:
            return self.__array[row, col]

        if self.__array_dimensions == 3:
            return self.__array[row, col, :]

        raise NotImplementedException

    ####################################################################################################################
    def get_width(self) -> int:
        """
        :return: number of columns in original image
        """
        return len(self.__array[0])

    ####################################################################################################################
    def get_height(self) -> int:
        """
        :return: number of rows in original image
        """
        return len(self.__array)

    ####################################################################################################################
    def __set_data_type(self) -> None:
        """
        Method to set data-type of image.
        """
        if self.__array.dtype == np.uint8:
            self.__image_data_type = ImageDataType.UINT8
            return

        if self.__array.dtype == np.uint16:
            self.__image_data_type = ImageDataType.UINT16
            return

        raise NotImplementedException


########################################################################################################################
if __name__ == '__main__':
    IMAGE = "images/JPEG/bunny.jpg"
    image_obj = Image(file_name=IMAGE)

    plt.figure()
    plt.imshow(image_obj.get_array())
    plt.show()
