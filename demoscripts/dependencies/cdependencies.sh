#!/bin/bash

# Reads a c file whose path is specified as a command line argument
# and returns the dependencies.

echo "DEPENDENCIES:"
rosie -wholefile -encode json c.dependencies $1 | sed 's/c\.//g' | jq '.[].subs[].dependency.subs[].header.text'
