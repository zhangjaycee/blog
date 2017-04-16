#!/bin/bash

if [ -n "$1" ]; then
    ADD_NUM=$1
else
    ADD_NUM=""
fi
./add_more.py $ADD_NUM
#jekyll build -s . -d /var/html/blog
jekyll build --lsi -s . -d /var/html/blog
