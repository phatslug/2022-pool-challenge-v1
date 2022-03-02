#!/bin/bash
clang-12 -O2 -ffast-math prep.c -o prep.out
clang-12 -O2 -ffast-math proc.c -o proc.out
#gcc prep.c -o prep.out
#gcc proc.c -o proc.out