#!/usr/bin/env python

import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64
from arbotix_msgs.srv import *
from itertools import permutations
from igraph import*


class BasicMovement():
    def __init__(self):
        rospy.init_node("BasicMovement")

        
        rate = rospy.get_param("~rate", 20)
        r = rospy.Rate(rate)
        tick = 1.0 / rate
        self.coxa_joint_r1 = rospy.get_param('~coxa_joint_r1', 'coxa_joint_r1')
        self.coxa_joint_r2 = rospy.get_param('~coxa_joint_r2', 'coxa_joint_r2')
        self.coxa_joint_r3 = rospy.get_param('~coxa_joint_r3', 'coxa_joint_r3')
        self.tibia_joint_r1 = rospy.get_param('~tibia_joint_r1', 'tibia_joint_r1')
        self.tibia_joint_r2 = rospy.get_param('~tibia_joint_r2', 'tibia_joint_r2')
        self.tibia_joint_r3 = rospy.get_param('~tibia_joint_r3', 'tibia_joint_r3')
        self.coxa_joint_l1 = rospy.get_param('~coxa_joint_l1', 'coxa_joint_l1')
        self.coxa_joint_l2 = rospy.get_param('~coxa_joint_l2', 'coxa_joint_l2')
        self.coxa_joint_l3 = rospy.get_param('~coxa_joint_l3', 'coxa_joint_l3')
        self.tibia_joint_l1 = rospy.get_param('~tibia_joint_l1', 'tibia_joint_l1')
        self.tibia_joint_l2 = rospy.get_param('~tibia_joint_l2', 'tibia_joint_l2')
        self.tibia_joint_l3 = rospy.get_param('~tibia_joint_l3', 'tibia_joint_l3')
        self.tail_joint_1 = rospy.get_param('~tail_joint_1', 'tail_joint_1')
        self.tail_joint_2 = rospy.get_param('~tail_joint_2', 'tail_joint_2')
        self.tail_joint_3 = rospy.get_param('~tail_joint_3', 'tail_joint_3')

        self.joints = [self.coxa_joint_r1, self.coxa_joint_r2, self.coxa_joint_r3, self.coxa_joint_l1, self.coxa_joint_l2, self.coxa_joint_l3, \
        self.tibia_joint_r1, self.tibia_joint_r2, self.tibia_joint_r3, self.tibia_joint_l1, self.tibia_joint_l2, self.tibia_joint_l3, \
        self.tail_joint_1, self.tail_joint_2, self.tail_joint_3]
        self.tibia_joints = [self.tibia_joint_r1, self.tibia_joint_r2, self.tibia_joint_r3, self.tibia_joint_l1, self.tibia_joint_l2, self.tibia_joint_l3]
        self.tibia_joints_l = [self.tibia_joint_l1, self.tibia_joint_l2, self.tibia_joint_l3]
        self.tibia_joints_r = [self.tibia_joint_r1, self.tibia_joint_r2, self.tibia_joint_r3]
        self.tail_joints = [self.tail_joint_1, self.tail_joint_2, self.tail_joint_3]
        self.default_joint_speed = rospy.get_param('~default_joint_speed', 1)

        # Initialize the servo services and publishers
        self.init_servos()

        # Subscribe the the 'joint_states' topic so we can know how the joints are positioned
        rospy.loginfo("Subscribing to joint_states...")
        
        self.joint_state = JointState()
        
        rospy.Subscriber('joint_states', JointState, self.update_joint_state)
        
        # Wait until we actually have joint state values
        while self.joint_state == JointState():
            rospy.sleep(1)

        #self.sit_down()
        #self.stand_up()
        self.move_tail_center()


    def init_servos(self):
        # Create dictionaries to hold the speed, position and torque controllers
        self.servo_speed = dict()
        self.servo_position = dict()
        # Connect to the set_speed services and define a position publisher for each servo
        rospy.loginfo("Waiting for joint controllers services...")
                
        for joint in sorted(self.joints):
            # The set_speed services
            set_speed_service = '/' + joint + '/set_speed'
            rospy.wait_for_service(set_speed_service)
            self.servo_speed[joint] = rospy.ServiceProxy(set_speed_service, SetSpeed, persistent=True)

            # Initialize the servo speed to the default_joint_speed
            self.servo_speed[joint](self.default_joint_speed)

            # The position controllers
            self.servo_position[joint] = rospy.Publisher('/' + joint + '/command', Float64, queue_size=5)

    def set_servo_position(self, servo, position):
        self.servo_position[servo].publish(position)	
    
    def stand_up(self):
	rospy.loginfo("center all servos")
		
	for joint in sorted(self.joints):
		self.set_servo_position(joint, 0)
			
	rospy.sleep(2)
		
    def sit_down(self):
	rospy.loginfo("standing up...")
		
	for joint in sorted(self.tibia_joints_r):
		self.set_servo_position(joint, 1.5)
	for joint in sorted(self.tibia_joints_l):
		self.set_servo_position(joint, -1.5)
	rospy.sleep(2)
    
    def move_one_step(self):
        rospy.loginfo("moving...")
        
        self.servo_speed[self.coxa_joint_r1](self.default_joint_speed)
        self.servo_speed[self.tibia_joint_r1](self.default_joint_speed)
        
        current_coxa_r1 = self.joint_state.position[self.joint_state.name.index(self.coxa_joint_r1)]
        current_tibia_r1 = self.joint_state.position[self.joint_state.name.index(self.tibia_joint_r1)]

       
        self.servo_position[self.coxa_joint_r1].publish(current_coxa_r1-1)
        self.servo_position[self.tibia_joint_r1].publish(current_tibia_r1+1)
        rospy.sleep(1)
        
    def move_tail_center(self):
	rospy.loginfo("moving tail...")
		
	self.set_servo_position(self.tail_joint_1, 0)
	self.set_servo_position(self.tail_joint_2, 0)
	self.set_servo_position(self.tail_joint_3, 0)
		
	rospy.sleep(1)
    def construction(self):
        perm = list(set(sorted(permutations([0,0,0,0,0,0,0.5,0.5,0.5,0.5,0.5,0.5], 6))))
        g = Graph.Full(64, directed = True)
        attr = ['r1','r2','r3','l1','l2','l3']
        for att in attr:
            g.vs[att] = [0]*64
        for i in range(len(perm)):
            g.vs['r1'][i]=perm[i][0]
            g.vs['r2'][i]=perm[i][1]
            g.vs['r3'][i]=perm[i][2]
            g.vs['l1'][i]=perm[i][3]
            g.vs['l2'][i]=perm[i][4]
            g.vs['l3'][i]=perm[i][5]
            
        weights = []
        for j in range(g.ecount()):
            weights.append(random.uniform(0,1))
        g.es['weight'] = weights
        mf = g.maxflow(0, 1)
        path = mf.partition
        for v in path[0]:
            self.set_servo_position(self.tibia_joint_r1, g.vs['r1'][v])
            self.set_servo_position(self.tibia_joint_r1, g.vs['r2'][v])
            self.set_servo_position(self.tibia_joint_r1, g.vs['r3'][v])
            self.set_servo_position(self.tibia_joint_r1, g.vs['l1'][v])
            self.set_servo_position(self.tibia_joint_r1, g.vs['l2'][v])
            self.set_servo_position(self.tibia_joint_r1, g.vs['l3'][v])
                    
    
    def update_joint_state(self, msg):
        try:
            #test = msg.name.index(self.coxa_joint_r1)
            self.joint_state = msg
        except:
            pass
if __name__ == '__main__':
    try:
        BasicMovement()
    except rospy.ROSInterruptException:
        rospy.loginfo("BasicMovement node terminated.")

