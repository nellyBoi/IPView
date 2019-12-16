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
import pixel_range_displays


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
                 image_display: ImageDisplay,
                 min_pixel_display: pixel_range_displays.MinimumPixelDisplay):
        """
        """
        self.ui = ui
        self.__image_display = image_display
        self.__min_pixel_display = min_pixel_display

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
        self.__min_pixel_display.set_text(value=int(self._current_image.get_processed_image_min()))
        self.__image_display.display_image()

        if write_to_stream:
            self.stream_display.append_row(
                'Pixel Scale Percent Minimum: ' + str(self._current_val))

        return

    ####################################################################################################################
    def reset(self) -> None:
        """
        Reset controls to default value.
        """
        self.__min_value_slider.setValue(AdjustMinimumValue.START_SLIDE_VALUE)
        self.__min_pixel_display.clear_text()

        return


########################################################################################################################
class AdjustMaximumValue(QSlider):
    """
    Class to control minimum slider and adjust pixels accordingly. When a new minimum is desired the pixel values will
    scale so the whole dynamic range of will be utilized scaled to the new minimum and maximum.
    """
    START_SLIDE_VALUE = 100
    MIN_SLIDE_VALUE = 0
    MAX_SLIDE_VALUE = 100

    ####################################################################################################################
    def __init__(self,
                 ui: ipview_ui.IPViewWindow,
                 image_display: ImageDisplay,
                 max_pixel_display: pixel_range_displays.MaximumPixelDisplay):
        """
        """
        self.ui = ui
        self.__image_display = image_display
        self.__max_pixel_display = max_pixel_display

        self.__max_value_slider = self.ui.max_value_slider
        super(AdjustMaximumValue, self).__init__()

        self.__max_value_slider.setValue(AdjustMaximumValue.START_SLIDE_VALUE)
        self.__max_value_slider.setMinimum(AdjustMaximumValue.MIN_SLIDE_VALUE)
        self.__max_value_slider.setMaximum(AdjustMaximumValue.MAX_SLIDE_VALUE)

        self._current_val = AdjustMaximumValue.START_SLIDE_VALUE
        self._current_image = None

        self.stream_display = StreamDisplay.StreamDisplay(ui=self.ui)

    ####################################################################################################################
    def adjust(self, write_to_stream: bool = True) -> None:
        """
        Method to change and maximum pixel value on user input.
        """
        self._current_val = self.__max_value_slider.value()
        # grab current image
        self._current_image = self.__image_display.get_process_factory()

        # use process factory to modify image
        self._current_image.adjust_range(new_max_percent=self._current_val)
        self.__max_pixel_display.set_text(value=int(self._current_image.get_processed_image_max()))
        self.__image_display.display_image()

        if write_to_stream:
            self.stream_display.append_row('Pixel Scale Percent Maximum: ' + str(self._current_val))

        return

    ####################################################################################################################
    def reset(self) -> None:
        """
        Reset controls to default value.
        """
        self.__max_value_slider.setValue(AdjustMaximumValue.START_SLIDE_VALUE)
        self.__max_pixel_display.clear_text()

        return
