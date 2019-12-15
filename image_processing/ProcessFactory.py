"""
Nelly Kane
11.24.2019
"""
from PyQt5.QtGui import QImage

import image as im
import numpy as np

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import qRgb
from PyQt5.QtGui import (QImage, QPixmap)
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget


########################################################################################################################
class ProcessFactory:

    ALLOWABLE_FORMATS = [im.ImageFormat.RGB.name, im.ImageFormat.RGBA.name, im.ImageFormat.GRAY.name]
    ALLOWABLE_DATA_TYPES = [im.ImageDataType.UINT8.name, im.ImageDataType.UINT16.name]

    gray_color_table = [qRgb(i, i, i) for i in range(256)]

    ####################################################################################################################
    def __init__(self, image: im.Image):
        """
        """
        self._image = image
        self.__processed_array = self._image.get_array().copy()
        self.__image_float = np.array(self._image.get_array(), dtype=float)  # for computation purposes

        # check that processed array is compatible with the ProcessFactory
        if not self.__compatible():
            raise im.NotImplementedException

        self.__original_size = [self._image.get_height(), self._image.get_width()]

        self.__image_min = 0
        self.__image_max = 0
        self.__set_image_range()

        # set cropped rows and columns as entire image
        self.__cropped_rows = [0, len(self.__processed_array) - 1]
        self.__cropped_cols = [0, len(self.__processed_array[0]) - 1]
        self.__cropped_upper_left = [0, 0]

    ####################################################################################################################
    def crop(self, rows: list, cols: list) -> None:
        """
        Method to slice this image and store in the object.
        :param rows: [rowMin, rowMax] list
        :param cols: [colMin, colMax] list
        """
        if rows[0] < 0:
            rows[0] = 0
        if rows[1] > self.__original_size[0]:
            rows[1] = self.__original_size[0]
        if cols[0] < 0:
            cols[0] = 0
        if cols[1] > self.__original_size[1]:
            cols[1] = self.__original_size[1]

        self.__cropped_rows = [x + self.__cropped_upper_left[0] for x in rows]
        self.__cropped_cols = [x + self.__cropped_upper_left[1] for x in cols]
        self.__cropped_upper_left = [self.__cropped_upper_left[0] + rows[0], self.__cropped_upper_left[1] + cols[0]]

        return

    ####################################################################################################################
    def revert_to_original(self) -> None:
        """
        Method to revert to original image as it was constructed.
        """
        self.__processed_array = self._image.get_array().copy()  # copy required to force contiguous memory
        self.__cropped_rows = [0, len(self.__processed_array) - 1]
        self.__cropped_cols = [0, len(self.__processed_array[0]) - 1]
        self.__cropped_upper_left = [0, 0]

        return

    ####################################################################################################################
    def save_image(self, file_name: str) -> None:
        """
        :param file_name: full path, name and extension to file.
        """
        self.to_QImage().save(file_name)

        return

    ####################################################################################################################
    def to_QImage(self) -> QImage:
        """
        A method to return the processed image as a QImage.
        :return: QImage object
        """
        row0 = self.__cropped_rows[0]
        row1 = self.__cropped_rows[1]
        col0 = self.__cropped_cols[0]
        col1 = self.__cropped_cols[1]
        if self._image.get_dimensions() == 2:
            array_cropped = self.__processed_array[row0: row1, col0: col1].copy()
        elif self._image.get_dimensions() == 3:
            array_cropped = self.__processed_array[row0: row1, col0: col1, :].copy()
        else:
            raise im.NotImplementedException

        if self._image.get_data_type() == im.ImageDataType.UINT8.name:
            if self._image.get_format() == im.ImageFormat.GRAY.name:
                q_image = QImage(array_cropped.data, array_cropped.shape[1], array_cropped.shape[0],
                                 array_cropped.strides[0], QImage.Format_Indexed8)
                q_image.setColorTable(ProcessFactory.gray_color_table)
                return q_image

            elif self._image.get_format() == im.ImageFormat.RGB.name:
                q_image = QImage(array_cropped.data, array_cropped.shape[1], array_cropped.shape[0],
                                 array_cropped.strides[0], QImage.Format_RGB888)  # 24-bit RGB format (8-8-8)
                return q_image

            elif self._image.get_format() == im.ImageFormat.RGBA.name:
                q_image = QImage(array_cropped.data, array_cropped.shape[1], array_cropped.shape[0],
                                 array_cropped.strides[0], QImage.Format_ARGB32)  # 32-bit RGBA format
                return q_image

        if self._image.get_data_type() == im.ImageDataType.UINT16.name:
            if self._image.get_format() == im.ImageFormat.GRAY.name:

                # TODO: Get new version of Qt. Current version doesn't support 16-bit grayscale so for now we will
                # convert to 8
                array8 = (array_cropped / 256).astype('uint8')
                q_image = QImage(array8.data, array8.shape[1], array8.shape[0], array8.strides[0],
                                 QImage.Format_Grayscale8)
                q_image.setColorTable(ProcessFactory.gray_color_table)
                return q_image

        raise im.NotImplementedException

    ####################################################################################################################
    def __compatible(self) -> bool:
        """
        :return: True if image has compatible format and data type
        """
        if self._image.get_format() not in ProcessFactory.ALLOWABLE_FORMATS:
            return False

        if self._image.get_data_type() not in ProcessFactory.ALLOWABLE_DATA_TYPES:
            return False

        return True

    ####################################################################################################################
    def __set_image_range(self) -> None:
        """
        Method to set range of image based on image type.
        """
        if self._image.get_data_type() == im.ImageDataType.UINT8.name:
            self.__image_min = 0
            self.__image_max = 255

        return

    ####################################################################################################################
    def __clamp(self, array: np.ndarray) -> np.ndarray:
        """
        :param array:
        :return:
        """
        array[array < self.__image_min] = self.__image_min
        array[array > self.__image_max] = self.__image_max

        return array


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
    IMAGE = "../image_containers/images/JPEG/bunny.jpg"
    import sys

    app = QApplication(sys.argv)

    image = im.Image(file_name=IMAGE)
    process_factory = ProcessFactory(image=image)
    w = Window()
    w.add_image(image=process_factory.to_QImage())
    w.show()

    process_factory.adjust_contrast(contrast_val=100)
    w2 = Window()
    w2.add_image(image=process_factory.to_QImage())
    w2.show()

    sys.exit(app.exec_())