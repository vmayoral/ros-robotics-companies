#!/bin/bash

# Count companies and substract the two headers
companies=$(expr $(awk '/\| / {a[$0]++} END{for(i in a) print i, a[i]}' $1 | wc -l) - 2)

# Update README's first line with new shield
tail -n +2 $1 > $1.aux && \
    (echo "![](https://img.shields.io/badge/ros%20robotics%20companies-$companies-4d4cf5.svg)" && cat $1.aux) > $1.aux2 && \
    rm $1 $1.aux && mv $1.aux2 $1


