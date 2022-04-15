#!/bin/bash
FILES="./ebay_data/ebay_data/*"
for f in $FILES
do
    python parser.py $f
done