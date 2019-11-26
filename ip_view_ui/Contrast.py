"""
Nelly Kane
11.24.2019
"""
from PyQt5.QtWidgets import QSlider

import ipview_ui
import StreamDisplay
import ImageDisplay


########################################################################################################################
class Contrast(QSlider):

    START_SLIDE_VALUE = 0
    MIN_SLIDE_VALUE = -100
    MAX_SLIDE_VALUE = 100

    # TODO Move this somewhere.
    ALLOWABLE_FORMATS = [4]  # [Format_RBG32]

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

        self.stream_display = StreamDisplay.StreamDisplay(ui=self.ui)

    ####################################################################################################################
    def adjust(self, write_to_stream: bool = True) -> None:
        """
        Method to change and control contrast on user input.
        """
        self._current_val = self.__contrast.value()
        # grab current image
        self._current_image = self.__image_display.get_displayed_image()
        # operate
        # place back image object
        # TODO Can we operate on the image in place? How do we extract the data from QImage?

        if write_to_stream:
            self.stream_display.append_row(str(self._current_val))

        return

    ####################################################################################################################
    def __new_contrast(self) -> None:
        """
        Method to compute new contrast. TODO Re-org maybe?
        """

    ####################################################################################################################
    def __compute_factor(self, c_level) -> float:
        """
        TODO: Fill
        """
        factor = 259 * (c_level + 255)/(255 * (259 - c_level))

    ####################################################################################################################
    def __check_format(self) -> bool:
        """
        :return: True if image has compatible format.
        """
        if self._current_image.format() in Contrast.ALLOWABLE_FORMATS:
            return True

        return False

    ####################################################################################################################
    def __clamp(self, value: int) -> int:
        """
        :param value: Value to be clamped
        :return: Value that fits in the bounds provided by this.
        """
