"""
file: buffer.py
author: Nelly Kane
date_originated: 10.23.2019

A collection of buffer objects.

TODO: two-directional travel
"""
import numpy as np

from image_containers import image as im


########################################################################################################################
class CircularBuffer:

    ####################################################################################################################
    def __init__(self, buffer_size: int = 5):
        """
        Constructor
        :param buffer_size: size of buffer
        """
        self.__buffer_size = buffer_size
        self.__data = [None] * buffer_size
        self.__current_index = 0

    ####################################################################################################################
    def push(self, image: im.Image) -> None:
        """
        :param image: instance of Image
        """
        self.__data[self.__current_index] = image
        self.__increment_index()

        return

    ####################################################################################################################
    def get_data_at_index(self, index: int = 0) -> im.Image:
        """
        Get data at specified index. Index may be out of range of the data since it will carry over circularly to allow
        one to use this class without having to keep track of their own circularity.
        :param index: index
        :return: image at circular index
        """
        index = index % self.__buffer_size
        return self.__data[index]  # TODO : Can raise or throw an error here.

    ####################################################################################################################
    def get_current_size(self) -> int:
        """
        :return:  current number of filled elements
        """
        return sum(1 for e in self.__data if e)

    ####################################################################################################################
    def clear(self) -> None:
        """
        clear the buffer
        """
        self.__data = [None] * self.__buffer_size
        self.__current_index = 0

        return

    ####################################################################################################################
    def __increment_index(self) -> None:
        """
        Increment index with circular method. For instance, if the buffer_size is 5, the order of the index upon
        incrementation would be [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, ...].
        """
        self.__current_index = (self.__current_index + 1) % self.__buffer_size


########################################################################################################################
if __name__ == '__main__':
    
    im_0 = im.Image(np.full((2, 2), 0, dtype=np.uint8))
    im_1 = im.Image(np.full((2, 2), 1, dtype=np.uint8))
    im_2 = im.Image(np.full((2, 2), 2, dtype=np.uint8))
    im_3 = im.Image(np.full((2, 2), 3, dtype=np.uint8))
    im_4 = im.Image(np.full((2, 2), 4, dtype=np.uint8))
    im_5 = im.Image(np.full((2, 2), 5, dtype=np.uint8))
    im_6 = im.Image(np.full((2, 2), 6, dtype=np.uint8))
    im_7 = im.Image(np.full((2, 2), 7, dtype=np.uint8))
    im_8 = im.Image(np.full((2, 2), 8, dtype=np.uint8))
    im_9 = im.Image(np.full((2, 2), 9, dtype=np.uint8))
    
    circular_buffer = CircularBuffer(buffer_size=3)
    
    circular_buffer.push(im_0)
    print('current size: ' + str(circular_buffer.get_current_size()))
    circular_buffer.push(im_1)
    print('current size: ' + str(circular_buffer.get_current_size()))
    circular_buffer.push(im_2)
    print('current size: ' + str(circular_buffer.get_current_size()))
    print(circular_buffer.get_data_at_index(index=0).get_pixel_value(x=1, y=1))
    print(circular_buffer.get_data_at_index(index=1).get_pixel_value(x=1, y=1))
    print(circular_buffer.get_data_at_index(index=2).get_pixel_value(x=1, y=1))
    circular_buffer.push(im_3)
    print(circular_buffer.get_data_at_index(index=3).get_pixel_value(x=1, y=1))
    circular_buffer.push(im_4)
    circular_buffer.push(im_5)
    circular_buffer.push(im_6)
    circular_buffer.push(im_7)
    circular_buffer.push(im_8)
    circular_buffer.push(im_9)
    print(circular_buffer.get_data_at_index(index=7).get_pixel_value(x=1, y=1))
    print(circular_buffer.get_data_at_index(index=8).get_pixel_value(x=1, y=1))
    print(circular_buffer.get_data_at_index(index=9).get_pixel_value(x=1, y=1))
    print('current size: ' + str(circular_buffer.get_current_size()))





