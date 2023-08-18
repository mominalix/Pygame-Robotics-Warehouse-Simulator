import pygame
import math
import time
" !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  robotic_arm Class !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"


class robotic_arm(pygame.sprite.Sprite):
    """
        This class represents the robot arm.
        It derives from the "Sprite" class in Pygame.
        """

    def __init__(self, robot):
        self.height_adjuster = True
        self.robot=robot
        self.Arm_angle = self.robot.rover_heading
        self.direction = True
        self.queue = []
        self.offset = 0
        self.Reposition = False

    def pick(self, polygon):
        #print("Pick command called for robot:",self.robot.id)
        if self.robot.pick == 0 and self.Reposition == False:
            #print("Pick command processing for robot:", self.robot.id)
            self.dir = self.rotate(polygon.rect.center)
            if self.dir == False:
                polygon.pick = True
                polygon.robo = self.robot.id
            return True
        if self.Reposition == True:
            return self.reposition(polygon)
        return False

    def drop(self, destination,block_list):
        if self.robot.pick == 1 and self.Reposition == False:
            direction = self.rotate(destination)
            if direction == False:
                self.robot.polygon.pick = False
                #self.robot.pick = 0
                # Robot is now empty
                self.robot.carry = False
                block_list.remove(self.robot.polygon)
                # Add shape colors
                if self.robot.polygon.color == 'r':
                    self.robot.red.add_shape()
                elif self.robot.polygon.color == 'g':
                    self.robot.green.add_shape()
                else:
                    self.robot.blue.add_shape()

        if self.Reposition == True:
            #print("Reposition called for robot:",self.robot.id)
            self.reposition(self.robot.polygon)
            if self.Reposition == False:
                self.robot.drop=False
                return True
        return False

    def rotate(self, destination):
        # Arm heading calibration
        if self.Arm_angle < 0:
            self.Arm_angle += 360
        if self.Arm_angle > 359:
            self.Arm_angle -= 360

        # Arm Heading adjustment towards polygon
        self.pointb = (destination[0]-self.robot.pos[0], destination[1]-self.robot.pos[1])
        self.angle = int(self.robot.angle_between((0, 0), self.pointb))
        if self.angle < 0:
            self.angle += 360
        if self.angle > 359:
            self.angle -= 360
        if self.Arm_angle != self.angle:
            self.direction = True
            if self.Arm_angle > self.angle:
                diff = self.Arm_angle - self.angle
                if diff >= 180:
                    self.Arm_angle += 1
                else:
                    self.Arm_angle -= 1
            elif self.Arm_angle < self.angle:
                diff = self.angle - self.Arm_angle
                if diff > 180:
                    self.Arm_angle -= 1
                else:
                    self.Arm_angle += 1
        else:
            self.height_adjust(destination)
        self.robot.arm_heading = self.Arm_angle-self.robot.rover_heading
        self.arm_calibration()

        # Arm Rotation
        self.frame_update()
        return self.direction

    def height_adjust(self,destination):
        # Arm offset from destination calculate
        if self.offset == 0:
            self.offset = int(math.sqrt(((destination[0] - (self.robot.pos[0]))**2)+((destination[1] - (self.robot.pos[1]))**2)))

        # Arm length increase
        if self.offset > 45:
            self.robot.arm_up_offset += 1
            self.offset -= 1

        # Arm reached destination
        if 0<self.offset <= 45:
            self.Reposition = True
            self.direction = False
            self.offset=0

        # Update Frame
        self.frame_update()

    def reposition(self, polygon):
        # Arm up offset readjustment
        if self.robot.arm_up_offset >= 1:
            self.robot.arm_up_offset -= 1
            self.frame_update()

        elif -1 > self.robot.arm_heading or self.robot.arm_heading > 1:

            # Arm heading calibration
            self.arm_calibration()

            # Arm heading readjustment
            if self.robot.arm_heading < 180:
                self.robot.arm_heading -= 1
            if self.robot.arm_heading >= 180:
                self.robot.arm_heading += 1

            # Update Frame
            self.frame_update()

        elif self.robot.pick == 0:
            #print(self.robot.id)
            self.robot.pick = 1
            self.offset = 0
            self.Reposition = False
            self.direction=True
            # Robot now carries polygon
            self.robot.carry=True
        elif self.robot.pick == 1:
            self.Reposition = False

        return True

    def arm_calibration(self):
        if self.robot.arm_heading < 0:
            self.robot.arm_heading += 360
        if self.robot.arm_heading > 359:
            self.robot.arm_heading -= 360

    def frame_update(self):
        self.robot.arm_rotated = pygame.transform.rotate(self.robot.arm,
                                                         self.robot.arm_heading + self.robot.rover_heading - 90)
        self.robot.arm_up_rotated = pygame.transform.rotate(self.robot.arm_up,
                                                            self.robot.arm_heading + self.robot.rover_heading - 90)
        self.robot.arm_rect = self.robot.arm_rotated.get_rect()
        self.robot.arm_up_rect = self.robot.arm_up_rotated.get_rect()

        # Arm Positioning
        self.robot.rect.center = self.robot.pos
        self.robot.rover_rect.center = [self.robot.size[0] / 2, self.robot.size[1] / 2]
        self.robot.arm_rect.center = self.robot.rover_rect.center
        self.robot.arm_up_rect.center = [self.robot.arm_rect.center[0] + self.robot.arm_up_offset * math.cos(
            (self.robot.arm_heading + self.robot.rover_heading) * math.pi / 180.0),
                                         self.robot.arm_rect.center[1] + self.robot.arm_up_offset * math.sin(
                                             -(self.robot.arm_heading + self.robot.rover_heading) * math.pi / 180.0)]