#!/bin/bash

# ## Initial way to count companies
# ## NOTE: before adding markers to the README. Markers take the form of:
# ##      <!-- !navigation! -->
# ##      <!-- !end_navigation! -->
# ##
# # Count companies and substract the two headers
# companies=$(expr $(awk '/\| / {a[$0]++} END{for(i in a) print i, a[i]}' $1 | wc -l) - 2)
# inactive_companies=$(expr $(awk '/\*Inactive\*/ {a[$0]++} END{for(i in a) print i, a[i]}' $1 | wc -l))
# closed_companies=$(expr $(awk '/\<ins\>Closed\<\/ins\>/ {a[$0]++} END{for(i in a) print i, a[i]}' $1 | wc -l))
# acquired_companies=$(expr $(awk '/\*\*Acquired\*\*/ {a[$0]++} END{for(i in a) print i, a[i]}' $1 | wc -l))

companies=$(expr $(grep -A 10000 "\!companies\!" $1 | grep -B 10000 "\!end-companies\!" | head -n -1 | tail -n +4 | wc -l))
closed_companies=$(expr $(grep -A 10000 "\!acquired\!" $1 | grep -B 10000 "\!end-acquired\!" | head -n -1 | tail -n +4 | grep "<ins>Closed</ins>" | wc -l))
total_acquired_inactive_closed_companies=$(expr $(grep -A 10000 "\!acquired\!" $1 | grep -B 10000 "\!end-acquired\!" | head -n -1 | tail -n +4 | wc -l))
acquired_companies=$(expr $(grep -A 10000 "\!acquired\!" $1 | grep -B 10000 "\!end-acquired\!" | head -n -1 | tail -n +4 | grep "**Acquired**" | wc -l))
inactive_companies=$(expr $(grep -A 10000 "\!acquired\!" $1 | grep -B 10000 "\!end-acquired\!" | head -n -1 | tail -n +4 | grep "*Inactive*" | wc -l))
navigation_companies=$(expr $(grep -A 10000 "\!navigation\!" $1 | grep -B 10000 "\!end-navigation\!" | head -n -1 | tail -n +4 | wc -l))
manipulation_companies=$(expr $(grep -A 10000 "\!manipulation\!" $1 | grep -B 10000 "\!end-manipulation\!" | head -n -1 | tail -n +4 | wc -l))
perception_companies=$(expr $(grep -A 10000 "\!perception\!" $1 | grep -B 10000 "\!end-perception\!" | head -n -1 | tail -n +4 | wc -l))

# Update README's first line with new shields
tail -n +2 $1 > $1.aux && \
    (echo "[![](https://img.shields.io/badge/ROS%20robotics%20companies-$companies-4d4cf5.svg)](https://github.com/vmayoral/ros-robotics-companies#active-companies) [![](https://img.shields.io/badge/ROS%20robotics%20companies%20acquired-$acquired_companies-00a679.svg)](https://github.com/vmayoral/ros-robotics-companies#companies-acquired-closed-or-inactive) [![](https://img.shields.io/badge/ROS%20navigation%20users-$navigation_companies-bdf271.svg)](https://github.com/vmayoral/ros-robotics-companies#navigation) [![](https://img.shields.io/badge/ROS%20manipulation%20users-$manipulation_companies-bdf271.svg)](https://github.com/vmayoral/ros-robotics-companies#manipulation) [![](https://img.shields.io/badge/ROS%20perception%20users-$perception_companies-bdf271.svg)](https://github.com/vmayoral/ros-robotics-companies#perception)" && cat $1.aux) > $1.aux2 && \
    rm $1 $1.aux && mv $1.aux2 $1

# summary
echo "companies: " $companies
echo "total_acquired_inactive_closed_companies: " $total_acquired_inactive_closed_companies
echo "acquired_companies: " $acquired_companies
echo "inactive_companies: " $inactive_companies
echo "closed_companies: " $closed_companies
echo "navigation_companies: " $navigation_companies
echo "manipulation_companies: " $manipulation_companies
echo "perception_companies: " $perception_companies