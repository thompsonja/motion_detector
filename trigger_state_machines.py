#!/usr/bin/env python
import datetime

TRIGGER_ACTIVE = 0
TRIGGER_INACTIVE = 1

LEVEL_ACTIVE = 2
LEVEL_INACTIVE = 3


class DefaultTriggerStateMachine(object):

  def __init__(self, active_high=True, initial_state=TRIGGER_INACTIVE, initial_value=False):
    self.initial_state = initial_state
    self.initial_value = initial_value
    self.history_length = 1
    self.active_high = active_high
    self.reset()

  def reset(self):
    self.output_state = self.initial_state
    self.history = [self.initial_value]
    
  def process(self, current_value):
    previous = self.history[0]
    self.history[0] = current_value
    if current_value and not previous:
      if self.active_high:
        self.output_state = TRIGGER_ACTIVE
      else:
        self.output_state = TRIGGER_INACTIVE
    if not current_value and previous:
      if self.active_high:
        self.output_state = TRIGGER_INACTIVE
      else:
        self.output_state = TRIGGER_ACTIVE
    return self.output_state


class TimedShutoffTriggerStateMachine(object):

  def __init__(self,
               min_active_duration_s,
               max_active_duration_s,
               active_high=True,
               initial_state=LEVEL_INACTIVE,
               initial_value=False):
    self.initial_state = initial_state
    self.initial_value = initial_value
    self.active_high = active_high
    self.min_active_duration_s = min_active_duration_s
    self.max_active_duration_s = max_active_duration_s
    self.reset()

  def reset(self):
    self.current_state = self.initial_state
    
  def process(self, current_value):
    self.output_state = None
    if current_value:
      self.last_active_time = now = datetime.datetime.now()
      if self.current_state == LEVEL_INACTIVE:
        if self.active_high:
          self.output_state = TRIGGER_ACTIVE
        else:
          self.output_state = TRIGGER_INACTIVE
        self.current_state = LEVEL_ACTIVE
        self.first_active_time = self.last_active_time
    
    if self.current_state == LEVEL_ACTIVE and self.should_deactivate():
      self.current_state = LEVEL_INACTIVE
      if self.active_high:
        self.output_state = TRIGGER_INACTIVE
      else:
        self.output_state = TRIGGER_ACTIVE
        
    return self.output_state

  def should_deactivate(self):
    
    seconds_since_last_active = (datetime.datetime.now() - self.last_active_time).total_seconds()
    seconds_since_first_active = (datetime.datetime.now() - self.first_active_time).total_seconds()
    return ((seconds_since_last_active > self.min_active_duration_s) or 
            (seconds_since_first_active > self.max_active_duration_s))
