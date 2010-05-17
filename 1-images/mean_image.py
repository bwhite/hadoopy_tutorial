#!/usr/bin/env python
"""Resize image and compute mean
"""
import base64

import Image
import StringIO
import hadoopy
import numpy as np


def mapper(key, value):
    """Take in an image (base64) and metadata, emits the image un-b64'd and metadata as a python object.

    Args:
        key: metadata
        value: image (raw)

    Yields:
        A tuple in the form of (key, value)
        key: shape (width, height)
        value: image as a uint8 byte string
    """
    shape = (50, 50)
    image = Image.open(StringIO.StringIO(value)).convert('L')
    image = image.resize(shape)
    yield shape, image.tostring()


def reducer(key, values):
    """

    Args:
        key: shape (width, height)
        values: image as a uint8 byte string

    Yields:
        A tuple in the form of (key, value)
        key: shape (width, height)
        value: mean image as a uint8 byte string
    """
    accum, cnt = 0, 0
    for value in values:
        accum += np.array(np.fromstring(value, dtype=np.uint8), dtype=np.uint32)
        cnt += 1
    accum /= cnt
    yield key, np.array(accum, np.uint8).tostring()


if __name__ == "__main__":
    if hadoopy.run(mapper, reducer):
        hadoopy.print_doc_quit(__doc__)
