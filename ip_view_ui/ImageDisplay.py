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
        self.ui.image_display.setScene(self)
        self.__q_graphics_view = self.ui.image_display

        # image currently on display
        self.__displayed_image = None

        # data members reserved for mouse events and the sharing of data between override methods.
        self.__orig_pos_scene = None
        self.__orig_pos_screen = None
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
        if image is not None:
            self.__displayed_image = image
            self.display_image()

        return

    ####################################################################################################################
    def previous_image(self) -> None:
        """
        Method for a signal from the previous push button.
        """
        image = self.ui.app_data.get_previous_image()
        if image is not None:
            self.__displayed_image = image
            self.display_image()

        return

    ####################################################################################################################
    def clear_display(self) -> None:
        """
         Method to clear the image display.
        """
        self.clear()
        self.ui.image_display.show()
        self.__displayed_image = None  # reset image held in object
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

        height = self.ui.image_display.sceneRect().height()
        width = self.ui.image_display.sceneRect().width()

        if event.button() == ImageDisplay.CROP_IMAGE:
            self.__button_clicked_type = ImageDisplay.CROP_IMAGE

            # cursor location
            self.__orig_pos_scene = xy
            self.__orig_pos_screen = event.screenPos()

            # rubber band for zoom feature
            self.__current_rubber_band = QRubberBand(QRubberBand.Rectangle)
            self.__current_rubber_band.setGeometry(QRect(self.__orig_pos_screen, self.__orig_pos_screen))
            self.__current_rubber_band.show()

        elif event.button() == ImageDisplay.PIXEL_FETCH:
            self.__button_clicked_type = ImageDisplay.PIXEL_FETCH

            # return if click is not in image scene
            if xy.x() < 0 or xy.x() >= width or xy.y() < 0 or xy.y() >= height:
                return

            self.stream_display.append_row('Pixel: row[{0:.2f}], col[{1:.2f}]'.format(xy.y(), xy.x()))

        return

    ####################################################################################################################
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Override method to move rubber band while mouse button is pressed.
        """
        if self.__button_clicked_type == ImageDisplay.CROP_IMAGE:
            xy = event.screenPos()
            current_pos_screen = QPoint(int(xy.x()), int(xy.y()))
            q_rect = self.__get_q_rect_from_corners(corner_one=self.__orig_pos_screen, corner_two=current_pos_screen,
                                                    scene_coordinates=False)
            self.__current_rubber_band.setGeometry(q_rect)

        return

    ####################################################################################################################
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Override method to complete crop of image.
        """
        if self.__button_clicked_type == ImageDisplay.CROP_IMAGE:
            self.__current_rubber_band.hide()
            self.__cropped_image_rect = self.__get_q_rect_from_corners(corner_one=self.__orig_pos_scene,
                                                                       corner_two=event.scenePos().toPoint(),
                                                                       scene_coordinates=True)

            # numpy slice parameters for image
            row_min = self.__cropped_image_rect.topLeft().y()
            row_max = self.__cropped_image_rect.bottomRight().y()
            col_min = self.__cropped_image_rect.topLeft().x()
            col_max = self.__cropped_image_rect.bottomRight().x()
            self.__displayed_image.crop(rows=[row_min, row_max], cols=[col_min, col_max])

            self.__crop_info_to_stream()
            self.display_image()

        return

    ####################################################################################################################
    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent):
        """
        Override method to display original image.
        """
        self.__button_clicked_type = ImageDisplay.IMAGE_REVERT
        self.__displayed_image.revert_to_original()
        self.display_image()
        self.stream_display.clear_text()
        self.stream_display.append_row("Image reverted to original")

        return

    ####################################################################################################################
    def display_image(self) -> None:
        """
        """
        self.clear()
        image_for_display = self.__displayed_image.to_QImage()
        self.addPixmap(QPixmap.fromImage(image_for_display))
        self.ui.image_display.setSceneRect(QRectF(image_for_display.rect()))

        # ensures scene rectangle (rect) fits in view port.
        self.ui.image_display.fitInView(self.ui.image_display.sceneRect(), Qt.KeepAspectRatio)
        self.ui.image_display.show()

        return

    ####################################################################################################################
    def __get_q_rect_from_corners(self, corner_one: QPoint, corner_two: QPoint,
                                  scene_coordinates: bool = False) -> QRect:
        """
        Method to return QRect box compatible with image indexing. The need for this function is to allow capabilities
        of zoom to be captured from a box creation in any direction, instead of forcing an upper-left to lower-right
        box creation.
        :param corner_one: a corner of either screen or scene
        :param corner_two: a corner opposite of corner_one
        :param scene_coordinates: True if corners are in scene coordinates. NOTE: If they are, QRect returned will be
            within scene QRect.
        :return: QRect in the format (QPoint [upper-left], QPoint[lower-right]) in input coordinates.
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

        # force corners to be within image if corners are in scene coordinates.
        if scene_coordinates:
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
        self.stream_display.append_row('Rows: {0:.2f}, Columns: {1:.2f}'.format(self.__cropped_image_rect.height(),
                                                                                self.__cropped_image_rect.width()))

    ####################################################################################################################
    def show(self) -> None:
        """
        TODO: Possibly remove
        """
        self.ui.image_display.show()
