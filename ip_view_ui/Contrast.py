"""
Nelly Kane
11.24.2019
"""
from PyQt5.QtWidgets import QSlider
from PyQt5.QtGui import QColor

import ImageDisplay
import StreamDisplay
import ipview_ui


########################################################################################################################
class Contrast(QSlider):
    START_SLIDE_VALUE = 0
    MIN_SLIDE_VALUE = -100
    MAX_SLIDE_VALUE = 100

    # TODO Move this somewhere.
    ALLOWABLE_FORMATS = [4, 5]  # [Format_RBG32, Format_ARBG32]
    MAX_IMAGE_VALUE = 255
    MIN_IMAGE_VALUE = 0

    ####################################################################################################################
    def __init__(self,
                 ui: ipview_ui.IPViewWindow,
                 image_display: ImageDisplay):
        """
        """
        self.ui = ui
        self.__image_display = image_display

        self.__contrast = self.ui.contrast_adjust
        super(Contrast, self).__init__()

        self.__contrast.setValue(Contrast.START_SLIDE_VALUE)
        self.__contrast.setMinimum(Contrast.MIN_SLIDE_VALUE)
        self.__contrast.setMaximum(Contrast.MAX_SLIDE_VALUE)

        self._current_val = Contrast.START_SLIDE_VALUE
        self._current_image = None
        self._contrast_factor = 1

        self.stream_display = StreamDisplay.StreamDisplay(ui=self.ui)

    ####################################################################################################################
    def adjust(self, write_to_stream: bool = True) -> None:
        """
        Method to change and control contrast on user input.
        """
        self._current_val = self.__contrast.value()
        # grab current image
        self._current_image = self.__image_display.get_displayed_image()

        if self.__format_compatible() is False:
            self.stream_display.append_row(
                'Image Format: ' + str(self._current_image.format) + ' not compatible with contrast adjust.')
            return

        # compute new contrast factor
        self._contrast_factor = 259 * (self._current_val + 255) / (
                    255 * (259 - self._current_val))  # note: needs to be stored as a float

        # loop over image and change pixel values
        self.__loop_image()

        if write_to_stream:
            self.stream_display.append_row(str(self._current_val))

        return

    ####################################################################################################################
    def __loop_image(self) -> None:
        """
        Method to loop image pixel by pixel and change RBG values to adjust contrast
        """
        for row in range(self._current_image.height()):
            for col in range(self._current_image.width()):
                color = self._current_image.pixelColor(row, col)  # QColor

                new_red = Contrast.__clamp(self._contrast_factor*(color.red() - 128) + 128)
                new_green = Contrast.__clamp(self._contrast_factor * (color.green() - 128) + 128)
                new_blue = Contrast.__clamp(self._contrast_factor * (color.blue() - 128) + 128)
                new_color = QColor(new_red, new_green, new_blue)

                self._current_image.setPixelColor(row, col, new_color)

        self.__image_display.show()

        return

    ####################################################################################################################
    def __format_compatible(self) -> bool:
        """
        :return: True if image has compatible format.
        """
        if self._current_image.format() in Contrast.ALLOWABLE_FORMATS:
            return True

        return False

    ####################################################################################################################
    @staticmethod
    def __clamp(value: int) -> int:
        """
        :param value: Value to be clamped
        :return: Value that fits in the bounds provided by this.
        """
        if value > Contrast.MAX_IMAGE_VALUE:
            return int(Contrast.MAX_IMAGE_VALUE)
        elif value < Contrast.MIN_IMAGE_VALUE:
            return int(Contrast.MIN_IMAGE_VALUE)
        else:
            return int(value)
