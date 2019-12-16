"""
Nelly Kane
12.15.2019
"""
from PyQt5.QtWidgets import QSlider
from PyQt5.QtGui import QColor

import ImageDisplay
import StreamDisplay
import ipview_ui

from image_processing import ProcessFactory


########################################################################################################################
class AdjustMinimumValue(QSlider):
    """
    Class to control minimum slider and adjust pixels accordingly. When a new minimum is desired the pixel values will
    scale so the whole dynamic range of will be utilized scaled to the new minimum and maximum.
    """
    START_SLIDE_VALUE = 0
    MIN_SLIDE_VALUE = 0
    MAX_SLIDE_VALUE = 100

    ####################################################################################################################
    def __init__(self,
                 ui: ipview_ui.IPViewWindow,
                 image_display: ImageDisplay):
        """
        """
        self.ui = ui
        self.__image_display = image_display

        self.__min_value_slider = self.ui.min_value_slider
        super(AdjustMinimumValue, self).__init__()

        self.__min_value_slider.setValue(AdjustMinimumValue.START_SLIDE_VALUE)
        self.__min_value_slider.setMinimum(AdjustMinimumValue.MIN_SLIDE_VALUE)
        self.__min_value_slider.setMaximum(AdjustMinimumValue.MAX_SLIDE_VALUE)

        self._current_val = AdjustMinimumValue.START_SLIDE_VALUE
        self._current_image = None

        self.stream_display = StreamDisplay.StreamDisplay(ui=self.ui)

    ####################################################################################################################
    def adjust(self, write_to_stream: bool = True) -> None:
        """
        Method to change and minimum pixel value on user input.
        """
        self._current_val = self.__min_value_slider.value()
        # grab current image
        self._current_image = self.__image_display.get_process_factory()

        # use process factory to modify image
        self._current_image.adjust_range(new_min_percent=self._current_val)
        self.__image_display.display_image()

        if write_to_stream:
            self.stream_display.append_row('Pixel Scale Percent Minimum: ' + str(self._current_val))

        return

    ####################################################################################################################
    def reset(self) -> None:
        """
        Reset controls to default value.
        """
        self.__min_value_slider.setValue(AdjustMinimumValue.START_SLIDE_VALUE)

        return
