#!/usr/bin/env python
import argparse
import cv2
import mog_difference
import motion_detector
import threading
import trigger
import trigger_state_machines
import video_input
import video_recorder


def debug_display(active, mask):
  if display == 'orig':
    orig = cv2.cvtColor(video.raw_frame, cv2.COLOR_BGR2RGB)
    cv2.imshow('frame', orig)
  elif display == 'gray':
    cv2.imshow('frame', video.frame)
  elif display == 'diff':
    cv2.imshow('frame', mask)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    video.final_image = True
    

def trigger_connection(active, mask):
  motion_trigger.process_input(active)


parser = argparse.ArgumentParser(description='Motion Detector')
parser.add_argument('-t', '--threshold', default=1000000, help='Threshold', required=False)
parser.add_argument('-v', '--version', default='mog', help='Subtractor version (mog or mog2)', required=False)
parser.add_argument('-l', '--loglevel', default=1, help='loglevel (0=None, 1=When active, 2=all)', required=False)
parser.add_argument('-r', '--rate', default=0.1, help='Learning Rate', required=False)
parser.add_argument('-d', '--display', default='diff', help='Debug Display (orig, gray, diff)', required=False)

args = vars(parser.parse_args())

# grab flags
threshold = float(args['threshold'])
loglevel = int(args['loglevel'])
display = args['display']
version = args['version']
rate = args['rate']

algo = mog_difference.MogDifference(version, rate)
video = video_input.VideoInput()
detector = motion_detector.MotionDetector(video, algo, threshold, loglevel)
detector.on_motion_status_updated.append(debug_display)
detector.on_motion_status_updated.append(trigger_connection)
state_machine = trigger_state_machines.TimedShutoffTriggerStateMachine(2,10)
motion_trigger = trigger.Trigger(state_machine)
recorder = video_recorder.VideoRecorder()
motion_trigger.on_active.append(recorder.start)
motion_trigger.on_inactive.append(recorder.stop)
detector.start()