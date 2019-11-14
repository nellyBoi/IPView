"""
Nelly Kane
11.12.2019
"""
from PyQt5.QtCore import (Qt, QRectF)
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QGraphicsScene, QWidget)

import image as im
import ipview_ui


########################################################################################################################
class ImageDisplay(QWidget):
    """
    A class to control the image display in the IPView GUI.
    """

    ####################################################################################################################
    def __init__(self,
                 ui: ipview_ui.IPViewWindow):
        """
        """
        self.ui = ui
        super(ImageDisplay, self).__init__()
        self.__scene = QGraphicsScene()
        self.ui.image_display.setScene(self.__scene)

    ####################################################################################################################
    def next_image(self) -> None:
        """
        Method for a signal from the next push button.
        """
        image = self.ui.app_data.get_next_image()
        self.__display_image(image=image)

        return

    ####################################################################################################################
    def previous_image(self) -> None:
        """
        Method for a signal from the previous push button.
        """
        image = self.ui.app_data.get_previous_image()
        self.__display_image(image=image)

        return

    ####################################################################################################################
    def clear_display(self) -> None:
        """
         Method to clear the image display.
        """
        self.__scene.clear()
        self.ui.image_display.show()

        return

    ####################################################################################################################
    def __display_image(self, image: im.Image) -> None:
        """
        """
        if image is not None:
            self.__scene.clear()
            self.__scene.addPixmap(QPixmap.fromImage(image))
            self.ui.image_display.setSceneRect(QRectF(image.rect()))
            # ensures scene rectangle (rect) fits in view port.
            self.ui.image_display.fitInView(self.ui.image_display.sceneRect(), Qt.KeepAspectRatio)
            self.ui.image_display.show()

        return

