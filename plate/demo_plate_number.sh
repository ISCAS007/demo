#!/bin/bash

for f in `ls images`
do
    echo $f
    gnome-open $f
    alpr $f
    sleep 3
done
