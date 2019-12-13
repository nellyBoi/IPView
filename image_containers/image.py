"""
:file: image.py
:author: Nelly Kane
:date_originated: 10.23.2019
:modifications: 12.07.2019

A module for holding, accessing and manipulating image data.
"""
import ntpath

import cv2
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
from PyQt5.QtGui import (QImage, QPixmap, qRgb)
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget


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
    ARGB = 2
    GRAY = 3


########################################################################################################################
class ImageDataType(Enum):
    """
    An enum to hold image data types compatible with Image class.
    """
    UINT8 = 1  # Unsigned integer (0 to 255)
    #UINT16 = 2  # Unsigned integer (0 to 65535) TODO Unimplemented

########################################################################################################################
class Image:
    """
    Class to hold image for image processing. The class stores two copies of the image as numpy array's; one copy is the
    original data as read (for revert purposes) and the other is the processed image.
    """
    gray_color_table = [qRgb(i, i, i) for i in range(256)]

    ####################################################################################################################
    def __init__(self, array: np.ndarray = None, path: str = None, file_name: str = None):
        """
        :param array: numpy nd array
        :param path: full path to file folder
        :param file_name: name of image file
        """
        if array is not None:
            self.__array_orig = array
            self.__name = 'from_array'

        else:
            if path is not None:
                file_name = path + file_name

            self.__array_orig = plt.imread(file_name, cv2.IMREAD_UNCHANGED).copy()
            self.__name = ntpath.basename(file_name)

        self.__array_dimensions = len(self.__array_orig.shape)
        self.__image_format = 0
        if self.__array_dimensions == 2:
            self.__image_format = ImageFormat.GRAY
        elif self.__array_dimensions == 3:
            if self.__array_orig.shape[2] == 3:
                self.__image_format = ImageFormat.RGB
            elif self.__array_orig.shape[2] == 4:
                self.__image_format = ImageFormat.ARGB

        if self.__image_format == 0:
            print('WARNING: Incompatible image format, may not work with all methods')

        self.__image_data_type = 0
        self.__set_data_type()

        self.__array_processed = self.__array_orig.copy()

        # display parameters, so that a crop of the image can be displayed/saved without cropping underlying data
        self.__cropped_rows = [0, len(self.__array_processed) - 1]
        self.__cropped_cols = [0, len(self.__array_processed[0]) - 1]

    ####################################################################################################################
    def replace_data(self, data: np.ndarray) -> None:
        """
        TODO: Figure this out better if it works.
        """
        self.__array_processed[:, :, :] = data

        return

    ####################################################################################################################
    def crop(self, rows: list, cols: list) -> None:
        """
        Method to slice this image and store in the object.
        :param rows: [rowMin, rowMax] list
        :param cols: [colMin, colMax] list
        """
        self.__cropped_rows = rows
        self.__cropped_cols = cols  # TODO clamp this is values are outside of image.

        return

    ####################################################################################################################
    def revert_to_original(self) -> None:
        """
        Method to revert to original image as it was constructed.
        """
        self.__array_processed = self.__array_orig.copy()  # copy required to force contiguous memory

        return

    ####################################################################################################################
    def get_name(self) -> str:
        """
        :return: file name
        """
        return self.__name

    ####################################################################################################################
    def get_processed_array(self) -> np.ndarray:
        """
        :return: Current numpy array.
        NOTE: This is not the original.
        """
        return self.__array_processed

    ####################################################################################################################
    def get_original_array(self) -> np.ndarray:
        """
        :return: Original numpy array.
        NOTE: This is the original, often needed to compute on image (i.e. increasing contrast since operating on
        already processed image may have undesired accumulations.
        """
        return self.__array_orig

    ####################################################################################################################
    def get_format(self) -> ImageFormat:
        """
        :return: Image format
        """
        return self.__image_format

    ####################################################################################################################
    def get_data_type(self) -> ImageDataType:
        """
        :return: Image data-type
        """
        return self.__image_data_type

    ####################################################################################################################
    def get_pixel(self, row: int, col: int) -> np.ndarray:
        """
        :param row: row value of pixel
        :param col: column value of pixel
        :return: All channels of pixel.
        NOTE: It is the responsibility of the user on the call side to know the ImageFormat.
        """
        if self.__array_dimensions == 2:
            return self.__array_processed[row, col]

        if self.__array_dimensions == 3:
            return self.__array_processed[row, col, :]

        raise NotImplementedException

    ####################################################################################################################
    def set_pixel(self, row: int, col: int, new_values: np.ndarray) -> None:
        """
        :param row: row value of pixel
        :param col: column value of pixel
        :param new_values: new values of pixel
        NOTE: It is the responsibility of the user on the call side to know the ImageFormat.
        """
        if self.__array_dimensions == 2:
            self.__array_processed[row, col] = new_values

        if self.__array_dimensions == 3:
            self.__array_processed[row, col, :] = new_values

        return

    ####################################################################################################################
    def current_width(self) -> int:
        """
        :return: number of columns in current image
        """
        return len(self.__array_processed[0])

    ####################################################################################################################
    def current_height(self) -> int:
        """
        :return: number of rows in current image
        """
        return len(self.__array_processed)

    ####################################################################################################################
    def original_width(self) -> int:
        """
        :return: number of columns in original image
        """
        return len(self.__array_orig[0])

    ####################################################################################################################
    def original_height(self) -> int:
        """
        :return: number of rows in original image
        """
        return len(self.__array_orig)

    ####################################################################################################################
    def save_image(self, file_name: str) -> None:
        """
        :param file_name: full path, name and extension to file.
        """
        pass

    ####################################################################################################################
    def to_QImage(self) -> QImage:
        """
        A method to convert an underlying numpy array of image data into a QImage object.
        :return: QImage object
        """
        row0 = self.__cropped_rows[0]
        row1 = self.__cropped_rows[1]
        col0 = self.__cropped_cols[0]
        col1 = self.__cropped_cols[1]
        if self.__array_dimensions == 2:
            array_cropped = self.__array_processed[row0: row1, col0: col1].copy()
        elif self.__array_dimensions == 3:
            array_cropped = self.__array_processed[row0: row1, col0: col1, :].copy()
        else:
            raise NotImplementedException

        if self.__array_processed.dtype == np.uint8:
            if self.__image_format == ImageFormat.GRAY:
                q_image = QImage(array_cropped.data, array_cropped.shape[1], array_cropped.shape[0],
                                 array_cropped.strides[0], QImage.Format_Indexed8)
                q_image.setColorTable(Image.gray_color_table)
                return q_image

            elif self.__image_format == ImageFormat.RGB:
                q_image = QImage(array_cropped.data, array_cropped.shape[1], array_cropped.shape[0],
                                 array_cropped.strides[0], QImage.Format_RGB888)  # 24-bit RGB format (8-8-8)
                return q_image

            elif self.__image_format == ImageFormat.ARGB:
                q_image = QImage(array_cropped.data, array_cropped.shape[1], array_cropped.shape[0],
                                 array_cropped.strides[0], QImage.Format_ARGB32)  # 32-bit ARGB format
                return q_image

        raise NotImplementedException

    ####################################################################################################################
    def __set_data_type(self) -> None:
        """
        Method to set data-type of image.
        """
        if self.__array_orig.dtype == np.uint8:
            self.__image_data_type = ImageDataType.UINT8
            return

        raise NotImplementedException

########################################################################################################################
class Window(QWidget):
    """
    Simple application window for rendering an image
    """

    def __init__(self):
        super(Window, self).__init__()

        # image label to display rendering
        self.img_label = QLabel(self)

    def add_image(self, image: QImage):
        """
        :param image: Image added to view chain.
        :return:
        """
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
    qimage0 = image.to_QImage()
    w = Window()
    w.add_image(image=qimage0)
    w.show()

    image.crop(rows=[100, 500], cols=[100, 900])
    qimage1 = image.to_QImage()
    w2 = Window()
    w2.add_image(image=qimage1)
    w2.show()

    sys.exit(app.exec_())
