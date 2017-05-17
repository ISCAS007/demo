#!/bin/bash

for f in `ls /home/yzbx/Pictures/platenumber*`
do
    echo $f
    gnome-open $f
    alpr $f
    sleep 3
done
