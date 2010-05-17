#!/usr/bin/env python
"""Runs the mean_image job
Usage:
python run_mean_image.py <hdfs_input>
"""
import hadoopy
import time
import sys
import Image
import re
import random


# Run job
def main(input_dir):
    output_dir = '/user/hadoop-trainer/output-ex1-0/%f' % (time.time())
    hadoopy.run_hadoop(input_dir, output_dir, 'mean_image.py')
    print('Output Dir:[%s]' % (output_dir))
    for key, val in hadoopy.hdfs_cat_tb(output_dir):
        fn = 'output-ex1-0-mean-%s.png' % ('-'.join(map(str, key)))
        print('Saving %s' % (fn))
        Image.fromstring('L', key, val).save(fn)

try:
    main(sys.argv[1])
except IndexError:
    print(__doc__)
