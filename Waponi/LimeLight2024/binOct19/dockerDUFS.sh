#!/bin/sh
# This is a simple script to run DUFS via docker. This allows web access to our data directory
# via port 5000. I'm not sure that this is the way to handle this process, as I want it
# to come up and down.

docker run -v ~/data:/data -p 5000:5000 --rm sigoden/dufs /data -A
