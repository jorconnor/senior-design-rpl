#!/bin/bash

echo not comment 1
<<COMMENT
echo comment 1
COMMENT
echo not comment 2
:<<COMMENT
echo comment 2
echo comment 2 cont.
COMMENT
echo not comment 3
<<'COMMENT'
echo comment 3
COMMENT
