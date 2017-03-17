#!/bin/bash

BASEDIR=$(dirname "$0")
echo "$BASEDIR"
cd $BASEDIR
make && make install