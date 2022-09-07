#!/bin/bash

# Count companies and substract the two headers
companies=$(expr $(awk '/\| / {a[$0]++} END{for(i in a) print i, a[i]}' $1 | wc -l) - 2)
inactive_companies=$(expr $(awk '/\*Inactive\*/ {a[$0]++} END{for(i in a) print i, a[i]}' $1 | wc -l))
closed_companies=$(expr $(awk '/\<ins\>Closed\<\/ins\>/ {a[$0]++} END{for(i in a) print i, a[i]}' $1 | wc -l))
acquired_companies=$(expr $(awk '/\*\*Acquired\*\*/ {a[$0]++} END{for(i in a) print i, a[i]}' $1 | wc -l))



# Update README's first line with new shields
tail -n +2 $1 > $1.aux && \
    (echo "[![](https://img.shields.io/badge/ros%20robotics%20companies-$companies-4d4cf5.svg)](https://github.com/vmayoral/ros-robotics-companies#active-companies) [![](https://img.shields.io/badge/acquired%20ros%20robotics%20companies-$acquired_companies-00a679.svg)](https://github.com/vmayoral/ros-robotics-companies#companies-acquired-closed-or-inactive)" && cat $1.aux) > $1.aux2 && \
    rm $1 $1.aux && mv $1.aux2 $1

# summary
echo "companies: " $companies
echo "acquired_companies: " $acquired_companies
echo "inactive_companies: " $inactive_companies
echo "closed_companies: " $closed_companies