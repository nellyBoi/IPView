"""
Nelly Kane
11.12.2019
"""
from PyQt5.QtCore import (Qt, QRectF, QRect, QSize, QPoint)
from PyQt5.QtGui import (QPixmap, QPainterPath)
from PyQt5.QtWidgets import (QGraphicsScene, QRubberBand, QGraphicsSceneMouseEvent)

import StreamDisplay
import image as im
import ipview_ui


########################################################################################################################
class ImageDisplay(QGraphicsScene):
    """
    A class to control the image display in the IPView GUI.
    """
    CROP_IMAGE = Qt.LeftButton
    PIXEL_FETCH = Qt.RightButton

    ####################################################################################################################
    def __init__(self,
                 ui: ipview_ui.IPViewWindow):
        """
        """
        self.ui = ui
        super(ImageDisplay, self).__init__()
        # self.__scene = QGraphicsScene()
        self.ui.image_display.setScene(self)
        self.__q_graphics_view = self.ui.image_display

        # image currently on display
        self.__displayed_image = None
        self.__displayed_image_orig = None

        # data members reserved for mouse events and the sharing of data between override methods.
        self.__orig_scene_pos = None
        self.__orig_screen_pos = None
        self.__current_rubber_band = None
        self.__cropped_image_rect = None
        self.__button_type = None

        self.stream_display = StreamDisplay.StreamDisplay(ui=self.ui)

    ####################################################################################################################
    def next_image(self) -> None:
        """
        Method for a signal from the next push button.
        """
        image = self.ui.app_data.get_next_image()
        self.__displayed_image_orig = image
        self.__display_image(image=image)

        return

    ####################################################################################################################
    def previous_image(self) -> None:
        """
        Method for a signal from the previous push button.
        """
        image = self.ui.app_data.get_previous_image()
        self.__displayed_image_orig = image
        self.__display_image(image=image)

        return

    ####################################################################################################################
    def clear_display(self) -> None:
        """
         Method to clear the image display.
        """
        self.clear()
        self.ui.image_display.show()
        self.__displayed_image = None  # reset image held in object
        self.__displayed_image_orig = None  # reset original image held in object
        self.__cropped_image_rect = None
        self.__button_type = None

        return

    ####################################################################################################################
    def get_displayed_image(self) -> im.Image:
        """
        :return: Image currently on display.
        """
        return self.__displayed_image

    ####################################################################################################################
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        """
        Override method of a mouse click event in QGraphicsView.
        - Left button provides the cropping feature.
        - Right button provides the pixel value.
        """
        if self.__displayed_image is None:
            return

        xy = event.scenePos().toPoint()
        x = xy.x()
        y = xy.y()

        height = self.ui.image_display.sceneRect().height()
        width = self.ui.image_display.sceneRect().width()

        # return if click is not in image scene
        if x < 0 or x >= width or y < 0 or y >= height:
            return

        if event.button() == ImageDisplay.CROP_IMAGE:
            self.__button_type = ImageDisplay.CROP_IMAGE  # TODO Do we need this?
            self.__orig_scene_pos = xy
            self.__orig_screen_pos = event.screenPos()
            self.__current_rubber_band = QRubberBand(QRubberBand.Rectangle, self.parent())
            self.__current_rubber_band.setGeometry(QRect(self.__orig_screen_pos, self.__orig_screen_pos))
            self.__current_rubber_band.show()

        elif event.button() == ImageDisplay.PIXEL_FETCH:
            self.__button_type = ImageDisplay.PIXEL_FETCH
            self.stream_display.append_row('Pixel: row[{0:.2f}], col[{1:.2f}]'.format(y, x))

        return

    ####################################################################################################################
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Override method to move rubber band while mouse button is pressed.
        """
        event_type = self.__button_type
        if event_type == ImageDisplay.CROP_IMAGE:
            xy = event.screenPos()
            pos_int = QPoint(int(xy.x()), int(xy.y()))
            self.__current_rubber_band.setGeometry(QRect(self.__orig_screen_pos, pos_int))

        return

    ####################################################################################################################
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Override method to complete crop of image.
        """
        if event.button() == ImageDisplay.CROP_IMAGE:

            self.__current_rubber_band.hide()
            self.__cropped_image_rect = QRect(self.__orig_scene_pos, event.scenePos().toPoint())
            self.__crop_info_to_stream()
            self.__current_rubber_band.deleteLater()
            cropped_image = self.__displayed_image.copy(self.__cropped_image_rect)
            self.__display_image(image=cropped_image)

        return

    ####################################################################################################################
    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent):
        """
        Override method to display original image.
        """
        if event.button() == ImageDisplay.CROP_IMAGE: # TODO :: Maybe revert should be a button instead??
            self.__display_image(image=self.__displayed_image_orig)
            self.stream_display.clear_text()
            self.stream_display.append_row("Image reverted to original")

        return

    ####################################################################################################################
    def __display_image(self, image: im.Image) -> None:
        """
        """
        if image is not None:
            self.clear()
            self.__displayed_image = image  # set reference to image in object
            self.addPixmap(QPixmap.fromImage(self.__displayed_image))
            self.ui.image_display.setSceneRect(QRectF(self.__displayed_image.rect()))

            # ensures scene rectangle (rect) fits in view port.
            self.ui.image_display.fitInView(self.ui.image_display.sceneRect(), Qt.KeepAspectRatio)
            self.ui.image_display.show()

        return

    ####################################################################################################################
    def __crop_info_to_stream(self) -> None:
        """
        Method to write image crop information to stream.
        """
        self.stream_display.append_row('Image Cropped, New Parameters: ')
        self.stream_display.append_row(str(self.__cropped_image_rect))
