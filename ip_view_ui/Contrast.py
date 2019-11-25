"""
Nelly Kane
11.24.2019
"""
from PyQt5.QtWidgets import (QSlider, QGraphicsSceneMouseEvent)

import ipview_ui
import StreamDisplay


########################################################################################################################
class Contrast(QSlider):

    START_SLIDE_VALUE = 0
    MIN_SLIDE_VALUE = -100
    MAX_SLIDE_VALUE = 100

    ####################################################################################################################
    def __init__(self,
                 ui: ipview_ui.IPViewWindow):
        """
        """
        self.ui = ui
        self = self.ui.contrastAdjust
        super(Contrast, self).__init__()

        self.setValue(Contrast.START_SLIDE_VALUE)
        self.setMinimum(Contrast.MIN_SLIDE_VALUE)
        self.setMaximum(Contrast.MAX_SLIDE_VALUE)

        self.stream_display = StreamDisplay.StreamDisplay(ui=self.ui)

    ####################################################################################################################
    def adjust(self) -> None:
        """
        Method to change and control contrast on user input.
        """
        self.stream_display.append_row('HELLO')

        return

    ####################################################################################################################
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        """
        Override method of a mouse click event in QGraphicsView.
        """
        self.adjust()

        return

    ####################################################################################################################
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Override method to move rubber band while mouse button is pressed.
        """
        self.adjust()

        return

    ####################################################################################################################
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Override method to adjust contrast of image.
        """
        self.adjust()

        return

    ####################################################################################################################
    def sliderMoved(self, position: int) -> None:
        """
        :param position: new position
        """
        self.adjust()

        return
