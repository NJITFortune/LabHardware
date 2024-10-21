#!/usr/bin/python

import sys

if len(sys.argv) > 1:
    if sys.argv[1] == "NoAudio":
        print(f'NoAudio was selected')
    else:
        print(f'Something else')
else:
    print(f'Nothing.')
