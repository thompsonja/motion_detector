#!/usr/bin/env python
import threading


class MotionDetector(object):

  def __init__(self, video_source, algo, threshold, loglevel):
    self.looping = False
    self.on_motion_status_updated = []

    self.video_source = video_source
    self.algo = algo
    self.threshold = threshold
    self.loglevel = loglevel
    
    self.loop_thread = threading.Thread(target=self.loop)

  def start(self):
    self.video_source.setup()
    self.looping = True
    self.loop_thread.start()    

  def stop(self):
    self.looping = False
    self.loop_thread.join()
    self.video_source.teardown()

  def loop(self):
    while(self.looping):
      self.video_source.update_frame()
      mask = self.algo.apply(self.video_source.frame)
      total = sum(map(sum, mask))
      active = total >= self.threshold
      
      for listener in self.on_motion_status_updated:
        listener(active, mask)
      
      # debug
      if self.loglevel >= 1 and active:
        print "ACTIVE %d" % total
      elif self.loglevel == 2:
        print total

      self.looping = not self.video_source.final_image