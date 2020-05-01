#! /usr/bin/env python
import rospy
import time         # for regular Python timing
import actionlib    # for actions!
from rico_actions.msg import \
    TimerAction, TimerGoal, TimerResult, TimerFeedback

def feedback_cb(feedback): # feedback callback function
  fb_elapsed = feedback.time_elapsed.to_sec()
  fb_remaining = feedback.time_remaining.to_sec()
  print('[Feedback] Time elapsed: %f' % (fb_elapsed))
  print('[Feedback] Time remaining: %f' % (fb_remaining))

rospy.init_node('timer_action_client') # initialize node
client = actionlib.SimpleActionClient( # register client
  'timer',    # action server name
  TimerAction # action Action message
)
client.wait_for_server()  # wait for action server
goal = TimerGoal()        # create goal object
goal.time_to_wait = rospy.Duration.from_sec(5.0) # set field
# Uncomment this line to test server-side abort:
# goal.time_to_wait = rospy.Duration.from_sec(500.0)

client.send_goal(goal, feedback_cb=feedback_cb) # send goal
# Uncomment these lines to test goal preemption:
# time.sleep(3.0)
# client.cancel_goal()

client.wait_for_result() # wait for action server to finish
# print results:
print('[Result] State: %d' % (client.get_state()))
print('[Result] Status: %s' % (client.get_goal_status_text()))
print('[Result] Time elapsed: %f' %
      (client.get_result().time_elapsed.to_sec()))
print('[Result] Updates sent: %d' % 
      (client.get_result().updates_sent))