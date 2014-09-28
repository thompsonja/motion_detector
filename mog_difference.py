#!/usr/bin/env python
import cv2


class MogDifference(object):

  def __init__(self, mog_type, learning_rate):
    # select diff algorithm
    if mog_type == 'mog':
      self.mog = cv2.BackgroundSubtractorMOG()
    else:
      self.mog = cv2.BackgroundSubtractorMOG2()
    self.learning_rate = learning_rate
      
  def apply(self, input):
    return self.mog.apply(input, None, self.learning_rate)