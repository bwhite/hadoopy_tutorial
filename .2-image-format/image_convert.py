#!/usr/bin/env python
"""Hadoopy Image Convert
Converts base64 encoded images to raw typed bytes (assuming the job is set to output this way).
"""
import base64

import hadoopy


def mapper(key, value):
    """Take in an image (base64) and metadata, emits the image un-b64'd and metadata as a python object.

    Args:
        key: byte offset
        value: tab delimited string of raw jpeg image data base64'd and metadata

    Yields:
        A tuple in the form of (metadata, image), where both are strings and the image is in raw bytes.
    """
    image, metadata = value.split('\t', 1)
    yield metadata, base64.b64decode(image)


if __name__ == "__main__":
    if hadoopy.run(mapper):
        hadoopy.print_doc_quit(__doc__)
