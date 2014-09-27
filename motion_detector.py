#!/usr/bin/env python
import argparse
import cv2
import threading


class MotionDetector(object):

  def __init__(self, args):
    self.looping = False

    # grab flags
    self.version = args['version']
    self.threshold = float(args['threshold'])
    self.loglevel = int(args['loglevel'])
    self.learning_rate = float(args['rate'])
    self.display = args['display']

    self.loop_thread = threading.Thread(target=self.loop)

  def start(self):
    # init webcam
    self.cap = cv2.VideoCapture(0)

    # select diff algorithm
    if self.version == 'mog':
      self.mog = cv2.BackgroundSubtractorMOG()
    else:
      self.mog = cv2.BackgroundSubtractorMOG2()

    self.looping = True
    self.loop_thread.start()    

  def stop(self):
    self.looping = False
    self.loop_thread.join()
    # When everything done, release the capture
    self.cap.release()
    cv2.destroyAllWindows()

  def loop(self):
    while(self.looping):

      # Capture frame-by-frame
      ret, frame = self.cap.read()
    
      # Our operations on the frame come here
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      mask = self.mog.apply(gray, None, self.learning_rate)

      # Calculate sum of white values
      total = sum(map(sum, mask))

      active = total >= self.threshold

      if self.loglevel >= 1 and active:
        print "ACTIVE %d" % total
      elif self.loglevel == 2:
        print total

      if self.display == 'orig':
        orig = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imshow('frame', orig)
      elif self.display == 'gray':
        cv2.imshow('frame', gray)
      elif self.display == 'diff':
        cv2.imshow('mask', mask)

      if cv2.waitKey(1) & 0xFF == ord('q'):
        self.looping = False
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Motion Detector')
  parser.add_argument('-t', '--threshold', default=1000000, help='Threshold', required=False)
  parser.add_argument('-v', '--version', default='mog', help='Subtractor version (mog or mog2)', required=False)
  parser.add_argument('-l', '--loglevel', default=1, help='loglevel (0=None, 1=When active, 2=all)', required=False)
  parser.add_argument('-r', '--rate', default=0.1, help='Learning Rate', required=False)
  parser.add_argument('-d', '--display', default='diff', help='Debug Display (orig, gray, diff)', required=False)
  argsDict = vars(parser.parse_args())
  detector = MotionDetector(argsDict)
  detector.start()