"""Takes a directory of images and packs them into a file that can be loaded into hadoop.
Usage:
python pack_images.py <input_dir> <output_file>
"""
import sys
import glob
import base64
import re

def main(in_dir, out_fn):
    with open(out_fn, 'w') as out_fp:
        for in_fn in glob.glob(in_dir + '/*.jpg'):
            with open(in_fn) as in_fp:
                metadata = in_fn.rsplit('/',1)[-1]
                b64img = base64.b64encode(in_fp.read())
                out_fp.write('%s\t%s\n' % (b64img, metadata))

if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2])
    except IndexError:
        print(__doc__)
        
