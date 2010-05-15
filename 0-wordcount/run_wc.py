import hadoopy
import time
import sys
import re

# Setup our input output dirs
try:
    run_count = int(sys.argv[1])
except IndexError:
    run_count = 0
input_dir = '/user/hadoop-trainer/input-ex0-%d' % (run_count)
output_dir = '/user/hadoop-trainer/output-ex0-%d/%f' % (run_count, time.time())

# Run job
print('Running input_dir[%s]' % (input_dir))
hadoopy.run_hadoop(input_dir, output_dir, 'wc.py')
print('Job Done. See your output (encoded in typedbytes, so it will have binary stuff around it) [hadoop fs -cat %s/part-00000]' % (output_dir))

# Dump from TypedBytes format
count_thresh = [1, 10000, 5, 5][run_count]
print("I'll read the data and dump it in a nicer form, look inside this file to see how to do this.  Only counts >= %d that match this regex '^[a-zA-Z\-,\.]+$' with length > 2 are output" % (count_thresh))
pairs = sorted(hadoopy.hdfs_cat_tb('%s/part-00000' % (output_dir)), lambda x,y: cmp(x[1], y[1]))
for key, val in pairs:
    if val >= count_thresh and re.search('^[a-zA-Z\-,\.]+$', key) and len(key) > 2:
        print('%s\t%s' % (key, val))

