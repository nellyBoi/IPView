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

    SCALE_RANGE = [0, 100]  # max assumed to be 100% of data-type range to start

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

        # set pixel value scaling parameters
        self.__pixel_min_percent = ProcessFactory.SCALE_RANGE[0]
        self.__pixel_max_percent = ProcessFactory.SCALE_RANGE[1]
        self.__processed_image_min = self.__image_min
        self.__processed_image_max = self.__image_max

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
    def adjust_range(self, new_min_percent: int = None, new_max_percent: int = None) -> None:
        """
        Method to adjust range of image. input parameters are as a percent. Values that fall outside of the percent
        values are set to their respective boundaries while values that are inside of the range are scaled to use the
        entire dynamic range of the image.
        :param new_min_percent: value in [0, 100]
        :param new_max_percent: value in [0, 100
        """
        if new_min_percent is None:
            new_min_percent = self.__pixel_min_percent
        if new_max_percent is None:
            new_max_percent = self.__pixel_max_percent

        if self._image.get_dimensions() != 2:
            print('3D images not implemented yet for this feature')  # TODO pass this to the stream.
            return

        if new_min_percent < ProcessFactory.SCALE_RANGE[0]:
            new_min_percent = ProcessFactory.SCALE_RANGE[0]
        if new_min_percent > ProcessFactory.SCALE_RANGE[1]:
            new_min_percent = ProcessFactory.SCALE_RANGE[1]
        if new_max_percent < ProcessFactory.SCALE_RANGE[0]:
            new_max_percent = ProcessFactory.SCALE_RANGE[0]
        if new_max_percent > ProcessFactory.SCALE_RANGE[1]:
            new_max_percent = ProcessFactory.SCALE_RANGE[1]

        if new_min_percent >= new_max_percent:
            self.__processed_array = np.zeros(shape=[self._image.get_height(), self._image.get_width()],
                                              dtype=self._image.get_array().dtype)
            return

        new_min = float(new_min_percent) / 100 * self.__image_max
        new_max = float(new_max_percent) / 100 * self.__image_max

        self.__processed_image_min = new_min
        self.__processed_image_max = new_max

        # reset parameters to new values
        self.__pixel_min_percent = new_min_percent
        self.__pixel_max_percent = new_max_percent

        scale_ratio = (self.__image_max - self.__image_min) / (new_max - new_min)
        current_image = self.__image_float.copy()

        current_image[current_image < new_min] = new_min
        current_image[current_image > new_max] = new_max

        if self._image.get_data_type() == im.ImageDataType.UINT8.name:
            self.__processed_array = np.array(np.multiply(np.subtract(current_image, new_min), scale_ratio),
                                              dtype=np.uint8)
            return

        if self._image.get_data_type() == im.ImageDataType.UINT16.name:
            self.__processed_array = np.array(np.multiply(np.subtract(current_image, new_min), scale_ratio),
                                              dtype=np.uint16)
            return

        raise im.NotImplementedException

    ####################################################################################################################
    def get_processed_image_min(self) -> int:
        """
        :return: Processed image minimum. NOTE: True min is zero after scaling.
        """
        return self.__processed_image_min

    ####################################################################################################################
    def get_processed_image_max(self) -> int:
        """
        :return: Processed image max. NOTE: True max is original image max after scaling.
        """
        return self.__processed_image_max

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
                                 array_cropped.strides[0], QImage.Format_RGBA8888)  # 32-bit RGBA format
                return q_image

        if self._image.get_data_type() == im.ImageDataType.UINT16.name:
            if self._image.get_format() == im.ImageFormat.GRAY.name:

                # TODO: Get new version of Qt. Current version doesn't support 16-bit grayscale so for now we will
                # convert to 8-bit
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

        if self._image.get_data_type() == im.ImageDataType.UINT16.name:
            self.__image_min = 0
            self.__image_max = 65535

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
