#!/usr/bin/python
from __future__ import division
from operator import add, sub, div, le, lt
import numpy as np
import cv2
import sys, os, re, collections

AVAILABLE_NUMBERS = [1, 2, 3]

for i in AVAILABLE_NUMBERS:
	image_name = str(i) + '.png'
	img = 