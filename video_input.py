#!/usr/bin/env python
import cv2


class VideoInput(object):

  def setup(self, index=0):
    self.cap = cv2.VideoCapture(index)
    self.final_image = False

  def teardown(self):
    self.cap.release()
    cv2.destroyAllWindows()

  def update_frame(self):
    ret, raw_frame = self.cap.read()
    self.frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2GRAY)
    self.raw_frame = raw_frame