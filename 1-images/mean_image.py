#!/usr/bin/env python
"""Resize image and compute mean
"""
import base64

import Image
import StringIO
import hadoopy
import numpy as np

class Mapper(object):
    def __init__(self):
        self.shape = (50, 50)

    def load_gray_image(self, jpeg_data):
        # Make File-like object from string, load image
        image = Image.open(StringIO.StringIO(jpeg_data))
        # Convert to gray
        return image.convert('L')
        
    def map(self, key, value):
        """Resize image and emit it.

        Args:
            key: metadata
            value: image (binary jpeg)

        Yields:
            A tuple in the form of (key, value)
            key: shape (width, height) (tuple)
            value: image (uint8 byte string)
        """
        image = self.load_gray_image(value)
        # Resize to a predefined shape
        image = image.resize(self.shape)
        # Using tostring produces a uint8 C-style array of the image
        # Some objects are more efficient to send as strings (images, arrays)
        yield self.shape, image.tostring()


class Reducer(object):
    def load_array(self, uint8_bytes):
        # Load uint8 data as a Numpy array (like matlab)
        arr = np.fromstring(uint8_bytes, dtype=np.uint8)
        # Convert it to uint32, we will sum these
        return np.array(arr, dtype=np.uint32)

    def reduce(self, key, values):
        """Sum up vectors, normalize, and emit.

        Args:
            key: shape (width, height)
            values: image as a uint8 byte string

        Yields:
            A tuple in the form of (key, value)
            key: shape (width, height) (tuple)
            value: mean image (uint8 byte string)
        """
        accum, cnt = 0, 0
        for value in values:
            accum += self.load_array(value)
            cnt += 1
        accum /= cnt
        # Using tostring produces a uint8 C-style array of the image
        # Some objects are more efficient to send as strings (images, arrays)
        yield key, np.array(accum, np.uint8).tostring()


if __name__ == "__main__":
    if hadoopy.run(Mapper, Reducer):
        hadoopy.print_doc_quit(__doc__)
