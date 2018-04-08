
## Initialize all at 0 

## Move L1, R2, L3 forward
self.set_servo_position(self.coxa_joint_l1, .5)
self.set_servo_position(self.tibia_joint_l1, .5)
self.set_servo_position(self.coxa_joint_l1, 0)

self.set_servo_position(self.coxa_joint_r2, .5)
self.set_servo_position(self.tibia_joint_r2, .5)
self.set_servo_position(self.coxa_joint_r2, 0)

self.set_servo_position(self.coxa_joint_l3, .5)
self.set_servo_position(self.tibia_joint_l3, .5)
self.set_servo_position(self.coxa_joint_l3, 0)



## Move R1, L2, R3 forward
self.set_servo_position(self.coxa_joint_r1, .5)
self.set_servo_position(self.tibia_joint_r1, .5)
self.set_servo_position(self.coxa_joint_r1, 0)

self.set_servo_position(self.coxa_joint_l2, .5)
self.set_servo_position(self.tibia_joint_l2, .5)
self.set_servo_position(self.coxa_joint_l2, 0)

self.set_servo_position(self.coxa_joint_r3, .5)
self.set_servo_position(self.tibia_joint_r3, .5)
self.set_servo_position(self.coxa_joint_r3, .0)

# Move L1, R2, L3 back to 0
self.set_servo_position(self.tibia_joint_l1, 0)
self.set_servo_position(self.tibia_joint_r2, 0)
self.set_servo_position(self.tibia_joint_l3, 0)



## Move L1, R2, L3 forward
self.set_servo_position(self.coxa_joint_l1, .5)
self.set_servo_position(self.tibia_joint_l1, .5)
self.set_servo_position(self.coxa_joint_l1, 0)

self.set_servo_position(self.coxa_joint_r2, .5)
self.set_servo_position(self.tibia_joint_r2, .5)
self.set_servo_position(self.coxa_joint_r2, 0)

self.set_servo_position(self.coxa_joint_l3, .5)
self.set_servo_position(self.tibia_joint_l3, .5)
self.set_servo_position(self.coxa_joint_l3, 0)

# Move R1, L2, R3 back to 0
self.set_servo_position(self.tibia_joint_r1, 0)
self.set_servo_position(self.tibia_joint_l2, 0)
self.set_servo_position(self.tibia_joint_r3, 0)