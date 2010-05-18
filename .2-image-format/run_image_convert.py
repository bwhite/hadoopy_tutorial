#!/usr/bin/env python
"""Runs the image_convert job
Usage:
python run_image_convert.py <hdfs_input> <hdfs_output>
"""
import hadoopy
import time
import sys
import re


# Run job
try:
    hadoopy.run_hadoop(sys.argv[1], sys.argv[2], 'image_convert.py', reducer=None)
except IndexError:
    print(__doc__)
