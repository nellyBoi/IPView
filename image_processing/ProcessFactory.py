"""
Nelly Kane
11.24.2019
"""
import image as im
import numpy as np

from PyQt5.QtWidgets import QApplication


########################################################################################################################
class ProcessFactory:
    MAX_IMAGE_VALUE = 255
    MIN_IMAGE_VALUE = 0

    MIN_CONTRAST_VALUE = -100
    MAX_CONTRAST_VALUE = 100

    ALLOWABLE_FORMATS = [im.ImageFormat.RGB]

    ####################################################################################################################
    def __init__(self):
        """

        self.__image_object = image
        self.__image_current = self.__image_object.get_array().copy()
        self.__contrast_factor = 0
        """

    ####################################################################################################################
    @staticmethod
    def adjust_contrast(image: im.Image, contrast_val: int) -> None:

        if contrast_val > ProcessFactory.MAX_CONTRAST_VALUE:
            contrast_val = ProcessFactory.MAX_CONTRAST_VALUE
        if contrast_val < ProcessFactory.MIN_CONTRAST_VALUE:
            contrast_val = ProcessFactory.MIN_CONTRAST_VALUE

        # compute new contrast factor  NOTE: needs to be stored as a float
        contrast_factor = 259 * (contrast_val + 255) / (255 * (259 - contrast_val))

        # loop over image and change pixel values
        current_image = np.array(image.get_array(), dtype=np.float)
        current_image = ProcessFactory.__clamp(contrast_factor * (current_image - 128) + 128)
        current_image = np.array(current_image, dtype=np.uint8)
        image.replace_data(data=current_image)

        return

    ####################################################################################################################
    def __format_compatible(self) -> bool:
        """
        :return: True if image has compatible format.
        """
        if self.__image_current.get_image_format() in ProcessFactory.ALLOWABLE_FORMATS:
            return True

        return False

    ####################################################################################################################
    @staticmethod
    def __clamp(array: np.ndarray) -> np.ndarray:
        """
        :param array:
        :return:
        """
        array[array < ProcessFactory.MIN_IMAGE_VALUE] = ProcessFactory.MIN_IMAGE_VALUE
        array[array > ProcessFactory.MAX_IMAGE_VALUE] = ProcessFactory.MAX_IMAGE_VALUE
        return array


########################################################################################################################
if __name__ == '__main__':
    IMAGE = "../image_containers/images/JPEG/bunny.jpg"
    import sys

    app = QApplication(sys.argv)

    image = im.Image(file_name=IMAGE)
    w = im.Window()
    w.add_image(image=image.to_QImage())
    print('image 1: ' + str(image.get_pixel(row=283, col=606)))
    w.show()

    ProcessFactory.adjust_contrast(image=image, contrast_val=-100)
    w2 = im.Window()
    w2.add_image(image=image.to_QImage())
    print('image 2: ' + str(image.get_pixel(row=283, col=606)))
    w2.show()

    sys.exit(app.exec_())
