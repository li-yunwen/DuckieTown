#!/usr/bin/env python3

import rospy
from std_msgs.msg import Header
from duckietown_msgs.msg import BoolStamped, WheelsCmdStamped
import smach


####### unfinished but will be done ASAP #############


class LaneFollowing(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['AprilTag_detected'])
        self.vehicle_name = 'pebbles'
    
    def execute(self, userdata):
        rospy.loginfo("Executing state: RUN")
        # DONE: execute line-following
        self.start_lane_following(self.vehicle_name)
        # TODO: subscribe AprilTag_detector
        return 'AprilTag_detected'

    def start_lane_following(self, vehicle_name):
        pub = rospy.Publisher(f'/{vehicle_name}/joy_mapper_node/joystick_override', BoolStamped, queue_size=10)
        
        msg = BoolStamped()
        msg.header = Header()
        msg.header.seq = 0
        msg.header.stamp = rospy.Time(0)
        msg.header.frame_id = ''
        msg.data = False 
        
        rospy.loginfo("Start lane following")
        pub.publish(msg)
        
        
class Stop(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['green'])
        self.vehicle_name = 'pebbles'
    
    def execute(self, userdata):
        rospy.loginfo("Executing state: STOP")
        # DONE: velocity turns to zero
        self.stop_lane_following(self.vehicle_name)
        # TODO: subscribe tp detector
        return 'green'
    
    def stop_lane_following(self, vehicle_name):
        pub = rospy.Publisher(f'/{vehicle_name}/joy_mapper_node/joystick_override', BoolStamped, queue_size=10)
        
        msg = BoolStamped()
        msg.header = Header()
        msg.header.seq = 0
        msg.header.stamp = rospy.Time(0)
        msg.header.frame_id = ''
        msg.data = True
        
        rospy.loginfo("Stop lane following")
        pub.publish(msg)

        pub_wheels_cmd = rospy.Publisher(f'/{vehicle_name}/wheels_driver_node/wheels_cmd', WheelsCmdStamped, queue_size=10)
        
        msg_wheels_cmd = WheelsCmdStamped()
        msg_wheels_cmd.header = Header()
        msg_wheels_cmd.header.seq = 0
        msg_wheels_cmd.header.stamp = rospy.Time(0)
        msg_wheels_cmd.header.frame_id = ''
        msg_wheels_cmd.vel_left = 0.0  
        msg_wheels_cmd.vel_right = 0.0 

        rospy.loginfo("Stopping wheels")
        pub_wheels_cmd.publish(msg_wheels_cmd)        


class Planning(smach.State): 
    def __init__(self):
        smach.State.__init__(self, outcomes=['plan_finished'])
    
    def execute(self, userdata):
        rospy.loginfo("Executing state: PLANNING")
        # TODO: wheel cmd do a quater circle
        return 'plan_finished'


class Turning(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['turn_finish'])
    
    def execute(self, userdata):
        rospy.loginfo("Executing state: TURN")
        # TODO: wheel cmd do a quater circle
        return 'turn_finish'
    

class AvoidingObstacle(smach.State): 
    def __init__(self):
        smach.State.__init__(self, outcomes=['obstacle_avoided'])
    
    def execute(self, userdata):
        rospy.loginfo("Executing state: AvoidingObstacel")
        # TODO: wheel cmd do a quater circle
        return 'obstacle_avoided'

class StateMachineNode:
    def __init__(self):
        rospy.init_node("state_machine_node")

        #  define state machine
        self.sm = smach.StateMachine(outcomes=['Run'])
        with self.sm:
            smach.StateMachine.add('Run', LaneFollowing(), transitions={'AprilTag_detected': 'Stop'})
            smach.StateMachine.add('Stop', Stop(), transitions={ 'turn': 'Turn'})
            smach.StateMachine.add('Turn', Turning(), transitions={'turn_finish': 'Run'})


    def run(self):
        outcome = self.sm.execute()




if __name__ == "__main__":
    print('State Machine start!')
    node = StateMachineNode()
    node.run()