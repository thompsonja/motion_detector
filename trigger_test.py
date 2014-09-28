#!/usr/bin/env python
import trigger
import unittest


active=0
inactive=0

def active_callback():
  global active
  active += 1
  
def inactive_callback():
  global inactive
  inactive += 1


def reset_callbacks():
  global active
  global inactive
  active = 0
  inactive = 0

  
class TriggerTest(unittest.TestCase):

  def setUp(self):
    self.trigger = trigger.Trigger()
    self.trigger.on_active.append(active_callback)
    self.trigger.on_inactive.append(inactive_callback)
    
  def tearDown(self):
    reset_callbacks()

  def testOneToggle(self):
    self.trigger.process_input(True)
    self.assertEqual(active, 1)
    self.assertEqual(inactive, 0)

  def testTwoToggles(self):
    self.trigger.process_input(True)
    self.trigger.process_input(False)
    self.assertEqual(active, 1)
    self.assertEqual(inactive, 1)

  def testUpdateState(self):
    pass
#    state_machine = trigger.DefaultTriggerStateMachine()
#    self.assertEqual(state_machine.process(True, True, True)   , trigger.TRIGGER_ACTIVE)
#    state_machine.reset()
#    self.assertEqual(state_machine.process(True, True, False)  , trigger.TRIGGER_INACTIVE)
#    state_machine.reset()
#    self.assertEqual(state_machine.process(True, False, True)  , trigger.TRIGGER_INACTIVE)
#    state_machine.reset()
#    self.assertEqual(state_machine.process(True, False, False) , trigger.TRIGGER_ACTIVE)
#    state_machine.reset()
#    self.assertEqual(state_machine.process(False, True, True)  , trigger.TRIGGER_ACTIVE)
#    state_machine.reset()
#    self.assertEqual(state_machine.process(False, True, False) , trigger.TRIGGER_INACTIVE)
#    state_machine.reset()
#    self.assertEqual(state_machine.process(False, False, True) , trigger.TRIGGER_INACTIVE)
#    state_machine.reset()
#    self.assertEqual(state_machine.process(False, False, False), trigger.TRIGGER_ACTIVE)

def runtests():
  unittest.main()

if __name__ == '__main__': runtests()