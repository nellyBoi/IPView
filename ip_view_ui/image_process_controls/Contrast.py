"""
Nelly Kane
11.24.2019
"""
from PyQt5.QtWidgets import QSlider
from PyQt5.QtGui import QColor

import ImageDisplay
import StreamDisplay
import ipview_ui

from image_processing import ProcessFactory


########################################################################################################################
class Contrast(QSlider):
    START_SLIDE_VALUE = 0
    MIN_SLIDE_VALUE = -100
    MAX_SLIDE_VALUE = 100

    # TODO Move this somewhere.
    #ALLOWABLE_FORMATS = [4, 5]  # [Format_RBG32, Format_ARBG32]
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

        # use process factory to modify image
        ProcessFactory.ProcessFactory.adjust_contrast(image=self._current_image, contrast_val=self._current_val)
        self.__image_display.display_image()

        if write_to_stream:
            self.stream_display.append_row('Contrast: ' + str(self._current_val))

        return

    ####################################################################################################################
    def reset(self) -> None:
        """
        Reset controls to default value.
        """
        self.__contrast.setValue(Contrast.START_SLIDE_VALUE)

        return

    ####################################################################################################################
    def __format_compatible(self) -> bool:
        """
        :return: True if image has compatible format.
        """
        if self._current_image.get_image_format() in ProcessFactory.ProcessFactory.ALLOWABLE_FORMATS:
            return True

        return True # TODO Figure out why this isn't working

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
