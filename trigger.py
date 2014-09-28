#!/usr/bin/env python
"""This is a simple trigger
"""

import trigger_state_machines


class Trigger(object):

  def __init__(self, state_machine=None):
    self.on_active = []
    self.on_inactive = []
    self.state_machine = state_machine or trigger_state_machines.DefaultTriggerStateMachine()
    self.state_machine.reset()

  def process_input(self, input):
    self.status = self.state_machine.process(input)
    if self.status == trigger_state_machines.TRIGGER_ACTIVE and self.on_active:
      for fn in self.on_active: fn()
    elif self.status == trigger_state_machines.TRIGGER_INACTIVE and self.on_inactive:
      for fn in self.on_inactive: fn()