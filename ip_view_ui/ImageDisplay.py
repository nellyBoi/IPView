"""
Nelly Kane
11.12.2019
"""
from PyQt5.QtCore import (Qt, QRectF, QRect, QPoint)
from PyQt5.QtGui import (QPixmap)
from PyQt5.QtWidgets import (QGraphicsScene, QRubberBand, QGraphicsSceneMouseEvent)

import StreamDisplay
import image as im
import ipview_ui


########################################################################################################################
class ImageDisplay(QGraphicsScene):
    """
    A class to control the image display in the IPView GUI.
    """
    # used to inform mouse event methods which button type is desired (i.e. mouse move or release)
    CROP_IMAGE = Qt.LeftButton
    PIXEL_FETCH = Qt.RightButton
    IMAGE_REVERT = 'PASS'

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
        self.__button_clicked_type = None

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
        self.__button_clicked_type = None

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
            self.__button_clicked_type = ImageDisplay.CROP_IMAGE
            self.__orig_scene_pos = xy
            self.__orig_screen_pos = event.screenPos()
            self.__current_rubber_band = QRubberBand(QRubberBand.Rectangle)
            self.__current_rubber_band.setGeometry(QRect(self.__orig_screen_pos, self.__orig_screen_pos))
            self.__current_rubber_band.show()

        elif event.button() == ImageDisplay.PIXEL_FETCH:
            self.__button_clicked_type = ImageDisplay.PIXEL_FETCH
            self.stream_display.append_row('Pixel: row[{0:.2f}], col[{1:.2f}]'.format(y, x))

        return

    ####################################################################################################################
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Override method to move rubber band while mouse button is pressed.
        """
        if self.__button_clicked_type == ImageDisplay.CROP_IMAGE:
            xy = event.screenPos()
            current_corner = QPoint(int(xy.x()), int(xy.y()))
            q_rect = self.__get_q_rect_from_points(corner_one=self.__orig_screen_pos, corner_two=current_corner)
            self.__current_rubber_band.setGeometry(q_rect)

        return

    ####################################################################################################################
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Override method to complete crop of image.
        """
        if self.__button_clicked_type == ImageDisplay.CROP_IMAGE:
            self.__current_rubber_band.hide()
            self.__cropped_image_rect = self.__get_q_rect_from_points(corner_one=self.__orig_scene_pos,
                                                                      corner_two=event.scenePos().toPoint())
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
        self.__button_clicked_type = ImageDisplay.IMAGE_REVERT
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
    def __get_q_rect_from_points(self, corner_one: QPoint, corner_two: QPoint) -> QRect:
        """
        Method to return QRect box compatible with image indexing. The need for this function is to allow capabilities
        of zoom to be captured from a box creation in any direction, instead of forcing an upper-left to lower-right
        box creation.
        :return: QRect in the format (QPoint [upper-left], QPoint[lower-right])
        Note: coordinate system is row -> y, col -> x
        """
        row_1 = corner_one.y()
        col_1 = corner_one.x()
        row_2 = corner_two.y()
        col_2 = corner_two.x()

        row_min = min(row_1, row_2)
        row_max = max(row_1, row_2)
        col_min = min(col_1, col_2)
        col_max = max(col_1, col_2)

        # force corners to be within image
        height = self.ui.image_display.sceneRect().height()
        width = self.ui.image_display.sceneRect().width()

        if row_min < 0:
            row_min = 0
        if col_min < 0:
            col_min = 0
        if row_max >= height:
            row_max = height - 1
        if col_max >= width:
            col_max = width - 1

        upper_left = QPoint(col_min, row_min)
        lower_right = QPoint(col_max, row_max)

        return QRect(upper_left, lower_right)

    ####################################################################################################################
    def __crop_info_to_stream(self) -> None:
        """
        Method to write image crop information to stream.
        """
        self.stream_display.append_row('Image Cropped, New Parameters: ')
        self.stream_display.append_row(str(self.__cropped_image_rect))
