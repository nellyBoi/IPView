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
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget

import cv2

########################################################################################################################


class NotImplementedException(BaseException):
    """
    Exception raised when a file-read was executed and the conversion to a QImage object is not possible due to an
    unimplemented file-type.
    """
    pass


########################################################################################################################
class FileExt(Enum):
    """
    Class to hold image file-extensions.
    """
    JPEG = 1
    TIF = 2
    PNG = 3


########################################################################################################################
class Image:
    """
    Class to hold a single image from a file-read or a numpy.array. The underlying data will be stored as a numpy.array
    and then passed to the display with a method that ports it's underlying data to a QImage object. Leaving the data as
    an array will make it faster for image processing, as opposed to leaving it as a QImage object, which would make
    the frame-to-frame display faster.
    """

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


            self.__name = ntpath.basename(file_name)

    ####################################################################################################################
    def get_name(self) -> str:
        """
        :return: file name
        """
        return self.__name

    ####################################################################################################################
    def convertToFormat(self, new_format: QImage.Format,
                        flags: Union[QtCore.Qt.ImageConversionFlags, QtCore.Qt.ImageConversionFlag] = None) -> 'Image':
        """
        Override method for converting image to a new format
        :param new_format: new QImage.Format
        :param flags: Union value
        :return: new Image object of type new_format.
        """
        if flags is None:
            new_image = super().convertToFormat(new_format)
        else:
            new_image = super().convertToFormat(new_format, flags)

        new_image.__class__ = Image

        return new_image

    ####################################################################################################################
    def to_QImage(self, im: np.ndarray, copy=False) -> None:
        """
        A method to convert an underlying numpy array of image data into a QImage object.
        :param im: numpy.ndarray of image data
        :param copy: boolean to copy underlying array
        :return: None
        TODO test this.
        """
        if im.dtype == np.uint8:
            if len(im.shape) == 2:
                super().__init__(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
                self.setColorTable(Image.gray_color_table)
                return
            elif len(im.shape) == 3:
                if im.shape[2] == 3:
                    super().__init__(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888)
                    return
                elif im.shape[2] == 4:
                    super().__init__(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_ARGB32)
                    return

        raise NotImplementedException

    ####################################################################################################################
    @staticmethod
    def __get_file_ext(file_name) -> FileExt:
        """
        :param file_name: file name
        :return:  file extension
        """
        file_ext = os.path.splitext(file_name)[-1]
        file_ext_enum = 0

        if ('jpg' in file_ext) or ('JPG' in file_ext):
            file_ext_enum = FileExt.JPEG

        if ('tif' in file_ext) or ('TIF' in file_ext):
            file_ext_enum = FileExt.TIF

        if ('png' is file_ext) or ('PNG' in file_ext):
            file_ext_enum = FileExt.PNG

        return file_ext_enum


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

    q_image = Image(file_name=IMAGE)
    if q_image.isNull():
        print('AN ISSUE GETTING THE IMAGE')

    else:
        print('IMAGE FORMAT: ' + str(q_image.format()))
        q_image = q_image.convertToFormat(QImage.Format_ARGB32)
        q_image.__class__ = Image
        print('NEW FORMAT: ' + str(q_image.format()))
        print('NEW IMAGE TYPE: ' + str(type(q_image)))

        w = Window(image=q_image)
        w.show()
        sys.exit(app.exec_())
