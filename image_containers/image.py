"""
:file: image.py
:author: Nelly Kane
:date_originated: 10.23.2019
:modifications: 11.30.2019

A module for holding, accessing and manipulating image data.
"""
import ntpath
import os
from enum import Enum
from typing import Union

import PyQt5.QtCore as QtCore
import numpy as np
from PyQt5.QtGui import (QImage, QPixmap, qRgb)
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget

import cv2
import matplotlib.pyplot as plt


########################################################################################################################
class NotImplementedException(BaseException):
    """
    Exception raised when a file-read was executed and the conversion to a QImage object is not possible due to an
    unimplemented file-type.
    """
    pass


########################################################################################################################
class Image:
    """
    Class to hold a single image from a file-read or a numpy.array. The underlying data will be stored as a numpy.array
    and then passed to the display with a method that ports it's underlying data to a QImage object. Leaving the data as
    an array will make it faster for image processing, as opposed to leaving it as a QImage object, which would make
    the frame-to-frame display faster.
    """
    gray_color_table = [qRgb(i, i, i) for i in range(256)]

    ####################################################################################################################
    def __init__(self, array: np.ndarray = None, path: str = None, file_name: str = None, **kwargs):
        """
        :param path: full path to file folder
        :param file_name: name of image file
        :param kwargs: RESERVED
        """
        if array is not None:
            self.__array = array
            self.__name = 'from_array'

        else:
            if path is not None:
                file_name = path + file_name

            self.__array = plt.imread(file_name, cv2.IMREAD_UNCHANGED)
            self.__name = ntpath.basename(file_name)

    ####################################################################################################################
    def get_name(self) -> str:
        """
        :return: file name
        """
        return self.__name

    ####################################################################################################################
    def to_QImage(self) -> QImage:
        """
        A method to convert an underlying numpy array of image data into a QImage object.
        :return: QImage object
        """
        if self.__array.dtype == np.uint8:
            if len(self.__array.shape) == 2:
                q_image = QImage(self.__array.data, self.__array.shape[1], self.__array.shape[0],
                                 self.__array.strides[0], QImage.Format_Indexed8)
                q_image.setColorTable(Image.gray_color_table)
                return q_image
            elif len(self.__array.shape) == 3:
                if self.__array.shape[2] == 3:
                    q_image = QImage(self.__array.data, self.__array.shape[1], self.__array.shape[0],
                                     self.__array.strides[0], QImage.Format_RGB888)  # 24-bit RGB format (8-8-8)
                    return q_image
                elif self.__array.shape[2] == 4:
                    q_image = QImage(self.__array.data, self.__array.shape[1], self.__array.shape[0],
                                     self.__array.strides[0], QImage.Format_ARGB32)  # 32-bit ARGB format
                    return q_image

        raise NotImplementedException


########################################################################################################################
class Window(QWidget):
    """
    Simple application window for rendering an image
    """

    def __init__(self, image: QImage):
        super(Window, self).__init__()

        # image label to display rendering
        self.img_label = QLabel(self)

        pix_map = QPixmap.fromImage(image)

        self.img_label.setPixmap(pix_map)
        self.img_label.setMinimumSize(1, 1)
        self.resize(pix_map.width(), pix_map.height())


########################################################################################################################
if __name__ == '__main__':

    IMAGE = "images/JPEG/bunny.jpg"
    import sys

    app = QApplication(sys.argv)

    image = Image(file_name=IMAGE)
    qimage = image.to_QImage()
    if qimage is None:
        print('AN ISSUE GETTING THE IMAGE')

    else:
        print('IMAGE FORMAT: ' + str(qimage.format()))

        w = Window(image=qimage)
        w.show()
        sys.exit(app.exec_())
