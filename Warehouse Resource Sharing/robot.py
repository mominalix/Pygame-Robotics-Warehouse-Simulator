import pygame
import pygame.freetype  # Import the freetype module.
import math
from polygon import polygon
from modules.path_planning import path_plannig
from modules.camera_module import camera_module
from modules.collision_avoidance import collision_avoidance
from modules.rescue import rescue
from modules.robotic_arm import robotic_arm
import numpy
import random
###### COLOUR DEFINATIONS ######

BLACK = (0, 0, 0, 0)
WHITE = (255, 255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 255, 255)

class robot(pygame.sprite.Sprite):
    """
        This class represents the robot.
        It derives from the "Sprite" class in Pygame.
        """

    def __init__(self, pos, name, red, green, blue, server,resource_sharing):
        pygame.sprite.Sprite.__init__(self)
        self.id = name
        self.img_addr = './data/'
        self.font = pygame.font.SysFont('Calibri', 16, False, False)
        # Collision Surface
        # self.safe_zone = polygon()
        # self.safe_zone.image = pygame.Surface((60, 60)).convert_alpha()
        # self.safe_zone.image.fill([245, 180, 180, 80])
        # self.safe_zone.rect = self.safe_zone.image.get_rect()
        # self.safe_zone.rect.center = pos
        # self.safe_zone.id = name
        # Rover
        self.rover = pygame.image.load(self.img_addr + "rover.png").convert_alpha()
        self.rover_heading = 0
        self.rover_rotated = pygame.transform.rotate(self.rover, self.rover_heading - 90)
        self.rover_rect = self.rover_rotated.get_rect()
        # Arm Lower
        self.arm = pygame.image.load(self.img_addr + "robo_arm_lower.png").convert_alpha()
        self.arm_heading = 0
        self.arm_rotated = pygame.transform.rotate(self.arm, self.arm_heading + self.rover_heading - 90)
        self.arm_rect = self.arm_rotated.get_rect()
        # Arm Upper
        self.arm_up = pygame.image.load(self.img_addr + "robo_arm_upper2.png").convert_alpha()
        self.arm_up_heading = 0
        self.arm_up_rotated = pygame.transform.rotate(self.arm_up, self.arm_up_heading + self.rover_heading - 90)
        self.arm_up_rect = self.arm_rotated.get_rect()
        # Arm move
        self.arm_up_offset = 0
        self.arm_open = 0
        self.arm_open_status = 0
        self.arm_open_status_prev = 0
        # Robo Initialize
        self.pos = pos
        self.vel = [0.5, 0.5]
        self.size = (200, 200)
        self.surface = pygame.Surface(self.size).convert_alpha()
        self.rect = self.surface.get_rect()
        self.rect.center = self.pos
        self.image_rect = self.rect
        self.rover_rect.center = [self.size[0] / 2, self.size[1] / 2]
        self.arm_rect.center = [self.size[0] / 2, self.size[1] / 2]
        self.arm_up_rect.center = [(self.size[0] / 2), (self.size[1] / 2)]
        self.surface.fill([255, 255, 255, 0])
        self.surface.blit(self.rover_rotated, self.rover_rect)
        self.surface.blit(self.arm_rotated, self.arm_rect)
        self.surface.blit(self.arm_up_rotated, self.arm_up_rect)
        self.increment = [0, 0, 0]
        # Robo Capabilities
        self.capable = ['CA', 'MV', 'CM', 'RA', 'OI']
        self.capable_available = {}
        for cap in self.capable:
            self.capable_available[cap] = 1
        self.capable_index = 0
        self.capable_disable = 0
        # Robo Status
        self.status = ['Moving', 'PPlanning', 'RGBDetect', 'RoboArm',
                       'Collision', 'Communicate', 'AIprocessor', 'Waiting']
        self.status_index = 7
        self.status__text = self.font.render(self.id + ':' + self.status[self.status_index], True, BLUE)

        # Robo pick and drop obj
        self.drop = False
        self.pick = 0
        self.pick_process = 'close'
        # RGB Detect
        self.RGB_block = ''
        # PP
        self.path_plan = 0
        self.path_selected = ''
        self.return_path = 0
        # MV
        self.move = 0
        self.move_pick = 0
        # Collision
        self.prev_pos = [self.pos[0], self.pos[1]]
        self.surface.blit(self.status__text, [self.size[1] / 2 - 50, self.size[1] / 2 + 50])
        self.adder = 1
        # Path Planning Class object
        self.increment[0] = - 1
        self.path_p = path_plannig(self, self.pos)
        self.robotic_arm = robotic_arm(self)
        self.i = 0
        self.Queue = []
        self.X = 0
        self.destination = self.pos
        # Server
        self.server=server
        # Racks
        self.red = red
        self.green = green
        self.blue = blue
        # Camera Module
        self.camera = camera_module()
        # Energy
        self.filename = "Graphs\\" + self.id + '.txt'
        self.plotfile = open(self.filename, "w")
        self.plotfile.close()
        self.energy = 100.0
        self.collision = 0
        self.iteration = 0
        self.polygon = None
        self.priority = 0
        self.robot_hit = None
        self.carry = False
        self.resource_sharing = resource_sharing
        self.Smart_collision = False
        # Halt flags
        self.halt_CA=False
        self.halt_MV=False
        self.halt_CM=False
        self.halt_RA=False
        self.halt_OI=False
        self.rescue = False
        self.direction=0

    def halt_check(self,block_list,robot_list):
        # -- Check Robot Collision
        self.collision = self.robot_collide(robot_list)
        if self.halt_CA==True:
            if self.capable_available['CA']==0:
                if self.collision == 0:
                    self.halt_CA = False
            else:
                self.halt_CA = False
        if self.halt_MV==True:
            if self.capable_available['MV']==0:
                return True
            else:
                self.halt_MV = False
        if self.halt_CM==True:
            if self.capable_available['CM']==0:
                if self.carry==1:
                    return True
            else:
                self.halt_CM = False
        if self.halt_RA==True:
            print("Halt detected for robot ",self.id)
            if self.capable_available['RA']==0:
                for polygon in block_list:
                    if ((-60 < (self.pos[0] - polygon.rect.center[0]) < 60 and -60 < (
                            self.pos[1] - polygon.rect.center[1]) < 60) or polygon.robo == self.id):
                        if polygon.robo=='R0' or polygon.robo==self.id:
                            return True
                return False
            else:
                self.halt_RA = False
        if self.halt_OI==True:
            if self.capable_available['OI']==0:
                if self.resource_sharing == True:
                    self.halt_OI = False
                if self.collision == 0:
                    for polygon in block_list:
                        if ((-60 < (self.pos[0] - polygon.rect.center[0]) < 60 and -60 < (
                                self.pos[1] - polygon.rect.center[1]) < 60) or polygon.robo == self.id):
                            if polygon.robo != self.id:
                                self.halt_OI = True
                                return True
                            else:
                                self.halt_OI = False
                else:
                    self.halt_OI = True
                    return True
            else:
                self.halt_OI = False
        return False

    def update_status(self, block_list, robot_safe_zone_list, robot_list,resource_sharing):
        # -- Update status
        self.resource_sharing = resource_sharing
        self.iteration += 1
        self.plotfile = open(self.filename, "a")
        self.plotfile.write(str(self.iteration) + ',' + str(self.energy) + '\n')
        self.plotfile.close()
        if self.energy > 0:
            self.energy-=0.001
            print(self.id, self.halt_RA)
            # -- Check Robot halt
            self.halt = self.halt_check(block_list,robot_list)
            if self.halt_MV== True:
                return
            if self.halt == True:
                return
            if self.carry==1 and self.capable_available['CM'] == 0 and self.resource_sharing == 0:
                self.halt_CM=True
                return
            print(self.id,self.carry,self.pick,self.halt,self.halt_RA)
            # if self.carry==1 and self.capable_available['RA'] == 0:
            #     return
            if self.collision==0 and self.Smart_collision == False:
                self.prev_pos = [self.pos[0], self.pos[1]]
                if self.capable_available['MV']==0 and self.carry==True:
                    self.payload_assist(robot_list)
                    self.halt_MV = True
                    return
                if self.capable_available['MV']==0 and self.carry==False:
                    self.halt_MV=True
                    return
                if self.capable_available['CM']==0 and self.resource_sharing==0 and self.carry==True:
                    return
                self.previous = self.pos
                self.prev_pos = [self.pos[0], self.pos[1]]

                # -- Rover heading calibration
                if self.rover_heading < 0:
                    self.rover_heading += 360
                if self.rover_heading > 359:
                    self.rover_heading -= 360
                self.capable_disable = 0

                # -- Resource sharing capabilities
                for cap in self.capable:
                    if self.capable_available[cap] == 0:
                        self.capable_disable = 1
                if self.capable_disable == 1:
                    self.status__text = self.font.render(self.id + ':Resorce Share Rqst ', True, BLUE)
                elif self.collision == 1:
                    self.status__text = self.font.render(self.id + ':COLLISION! ', True, BLUE)
                else:
                    self.status__text = self.font.render(self.id + ':Searching..', True, BLUE)
                if self.pos[0] - 2 < self.destination[0] < self.pos[0] + 2:
                    if self.pos[1] - 2 < self.destination[1] < self.pos[1] + 2:
                        self.status__text = self.font.render(self.id + ':Searching..', True, BLUE)
                        self.destination = self.path_p.plan_path()
                self.pointB = (self.destination[0] - self.pos[0], self.destination[1] - self.pos[1])
                self.angle = int(self.angle_between((0, 0), self.pointB))

                # -- Robot Rotation towards Destination
                if self.rover_heading != self.angle:
                    if self.rover_heading > self.angle:
                        diff = self.rover_heading - self.angle
                        if diff > 180:
                            self.body_rotate(1)
                        else:
                            self.body_rotate(-1)
                    elif self.rover_heading < self.angle:
                        diff = self.angle - self.rover_heading
                        if diff > 180:
                            self.body_rotate(-1)
                        else:
                            self.body_rotate(1)
                self.collision = 0
                polygon_pick = False

                # -- Polygon pick
                if self.pick == 0:
                    polygon_pick = self.polygon_collide(block_list, robot_list)
                if self.carry==True and self.resource_sharing == True:
                    self.search_assist(block_list, robot_list)

                # -- Rover Heading Adjustment
                if not polygon_pick and self.drop == False:
                    self.robotic_arm.Arm_angle = self.rover_heading
                    if self.angle - 2 < self.rover_heading < self.angle + 2:
                        try:
                            if self.capable_available['MV']==1:
                                self.movement()
                        except:
                            pass
                self.collision = self.robot_collide(robot_list)

                # -- If robot has picked polygon
                if self.pick == 1:
                    try:
                        self.priority = self.polygon.priority
                    except:
                        self.priority = 0
                    self.color='0'
                    self.shape='0'

                    # -- Camera Module for Polygon Identification
                    self.camera_assist()
                    self.status__text = self.font.render(self.id + ':Dropping polygon', True, BLUE)

                    # -- Polygon drop
                    if (self.destination[0] - 40 < self.polygon.rect.center[0] < self.destination[0] + 40) and (
                            self.destination[1] - 40 < self.polygon.rect.center[1] < self.destination[1] + 40):
                        self.drop = True
                        if self.capable_available['RA']==1:
                            self.drop_success = self.drop_polygon(block_list, self.color)
                            if self.drop_success== 1:
                                self.destination = self.path_p.plan_path()
                                self.rescue=False
                        else:
                            self.halt_RA=True
                            self.payload_assist(robot_list)
                            #self.destination=self.path_p.plan_path()
                            return

                # -- Object identifier
                if self.capable_available['OI'] == 0 and self.resource_sharing == False:
                    for polygon in block_list:
                        if ((-60 < (self.pos[0] - polygon.rect.center[0]) < 60 and -60 < (
                                self.pos[1] - polygon.rect.center[1]) < 60) or polygon.robo == self.id):
                            if polygon.robo!= self.id:
                                self.halt_OI = True
                                return

            # -- Halt checks
            if self.collision == 1:
                if self.capable_available['OI']==0 and self.resource_sharing == False:
                    self.halt_OI = True
                    return
                if self.capable_available['CA']==0 and self.resource_sharing == False:
                    self.halt_CA=True
                    return

            # -- Collision Detection
            if self.collision == 1 or self.Smart_collision==True:
                # Collision Avoidance
                self.collision = 0
                self.status__text = self.font.render(self.id + ':COLLISION!', True, BLUE)
                skip =False
                if self.carry==True or self.rescue == True:
                    if self.rescue == True:
                        for polygon in block_list:
                            if (-60 < (self.destination[0] - polygon.rect.center[0]) < 60 and -60 < (self.destination[1] - polygon.rect.center[1]) < 60):
                                skip=True
                    if  skip== False:
                        self.smart_collision(robot_list)
                    else:
                        self.destination = self.path_p.plan_path()
                        self.pos = self.prev_pos
                        self.smart_collision(robot_list)
                else:
                    self.destination = self.path_p.plan_path()
                    self.pos=self.prev_pos
                    self.smart_collision(robot_list)
            self.prev_pos = [self.pos[0], self.pos[1]]

        # Energy Low
        else:
            self.energy=0
            self.status__text = self.font.render(self.id + ':Energy low!', True, BLUE)
            self.payload_assist(robot_list)

        # Rover update
        self.surface.fill([255, 255, 255, 0])
        self.surface.blit(self.rover_rotated, self.rover_rect)
        self.surface.blit(self.arm_rotated, self.arm_rect)
        self.surface.blit(self.arm_up_rotated, self.arm_up_rect)
        self.surface.blit(self.status__text, [self.size[1] / 2 - 50, self.size[1] / 2 + 50])

    def movement(self):
        # - Path planning module
        self.Queue = self.path_p.create_path(self.destination)
        self.Queue.pop(0)
        self.pos = self.Queue.pop(0)
        self.pos = self.rect.center
        try:
            self.rect.center = self.Queue.pop(0)
        except:
            pass
        self.pos = self.rect.center
        self.rover_rect.center = [self.size[0] / 2, self.size[1] / 2]
        self.arm_rect.center = self.rover_rect.center
        self.arm_up_rect.center = [self.arm_rect.center[0] + self.arm_up_offset * math.cos(
            (self.arm_heading + self.rover_heading) * math.pi / 180.0),
                                   self.arm_rect.center[1] + self.arm_up_offset * math.sin(
                                       -(self.arm_heading + self.rover_heading) * math.pi / 180.0)]

    def drop_polygon(self, block_list, color):
        if self.capable_available['RA']==0:
            self.halt_RA = True
            if self.resource_sharing==1:
                self.payload_assist()
                self.destination=self.path_p.plan_path()
                self.carry=False
                self.pick=0
            return
        placed = self.robotic_arm.drop(self.destination, block_list)
        if placed == True:
            self.pick = 0
            if color == "red":
                self.energy -= 6
            if color == "blue":
                self.energy -= 4
            if color == "green":
                self.energy -= 2
            self.priority = 0
            return 1
        return 0

    def angle_between(self, p1, p2):
        ang1 = math.atan2(p1[1], p1[0])
        ang2 = math.atan2(p2[1], p2[0])
        r = ((ang1 - ang2) * (180.0 / math.pi))
        if r < 0:
            r += 360
        return r

    def body_rotate(self, direction):
        self.energy -= 0.001
        # -- Rotate whole rover
        self.rover_rotated = pygame.transform.rotate(self.rover, self.rover_heading - 90)
        self.rover_rect = self.rover_rotated.get_rect()
        # -- Rotate ARM
        self.arm_rotated = pygame.transform.rotate(self.arm, self.arm_heading + self.rover_heading - 90)
        self.arm_rect = self.arm_rotated.get_rect()
        # -- Rotate arm upper
        self.arm_up_rotated = pygame.transform.rotate(self.arm_up, self.arm_heading + self.rover_heading - 90)
        self.arm_up_rect = self.arm_up_rotated.get_rect()
        if direction == 1:
            self.rover_heading += 1
        else:
            self.rover_heading -= 1
        self.rect.center = self.pos
        self.rover_rect.center = [self.size[0] / 2, self.size[1] / 2]
        self.arm_rect.center = self.rover_rect.center
        self.arm_up_rect.center = [self.arm_rect.center[0] + self.arm_up_offset * math.cos(
            (self.arm_heading + self.rover_heading) * math.pi / 180.0),
                                   self.arm_rect.center[1] + self.arm_up_offset * math.sin(
                                       -(self.arm_heading + self.rover_heading) * math.pi / 180.0)]

    def robot_collide(self, robot_list):
        collision_detect = 0
        robot_hit_list = robot_list
        for self.robot_hit in robot_hit_list:
            if self.id != self.robot_hit.id:
                if (-100 < (self.pos[0] - self.robot_hit.pos[0]) < 100 and -100 < (
                        self.pos[1] - self.robot_hit.pos[1]) < 100):
                    collision_detect = 1
                    self.robot_hit = None
                    return collision_detect
        return collision_detect

    def polygon_collide(self, block_list,robot_list):
        for polygon in block_list:
            if ((-60 < (self.pos[0] - polygon.rect.center[0]) < 60 and -60 < (
                    self.pos[1] - polygon.rect.center[1]) < 60) or polygon.robo == self.id):
                if polygon.robo == 'R0' and self.capable_available['RA'] == 0:
                    self.pos = self.prev_pos
                    self.search_assist(block_list,robot_list)
                    self.destination =self.path_p.plan_path()
                    return False
                if polygon.robo == self.id or polygon.robo == 'R0':
                    self.polygon = polygon
                    self.status__text = self.font.render(self.id + ':Picking Polygon', True, BLUE)
                    if self.capable_available['RA'] == 0:
                        self.payload_assist(robot_list)
                        self.pos = self.prev_pos
                        self.halt_RA = True
                        return
                    else:
                        return self.robotic_arm.pick(polygon)
                if self.polygon == polygon and polygon.robo != self.id:
                    self.polygon = None
        return False

    def priority_check(self, robot_list):
        for self.robot_hit in robot_list:
            try:
                if self.robot_hit.robot_hit.id == self.id and self.robot_hit.id != self.id and self.robot_hit.carry == True:
                    self.smart_collision(robot_list)
                    return False
            except:
                pass
            try:
                x=self.robot_hit.pos[0]
            except:
                return False
            if (-100 < (self.pos[0] - self.robot_hit.pos[0]) < 100 and -100 < (
                    self.pos[1] - self.robot_hit.pos[1]) < 100 and self.robot_hit.id != self.id):
                if self.robot_hit.collision == 0 and self.robot_hit.energy > 0:
                    return True
                else:
                    return False

    def payload_assist(self, robot_list):
        if (self.carry == True or self.capable_available['MV']==0) and self.resource_sharing == True:
            for rover in robot_list:
                if rover.carry == False and rover.energy > 0 and rover.resource_sharing == True and rover.capable_available['MV']==1 and rover.capable_available['RA']==1:
                    rover.destination = self.polygon.rect.center
                    rover.rescue = True
                    try:
                        self.carry = False
                        self.polygon.pick = False
                        self.polygon.robo = 'R0'
                        self.pick =0

                    except:
                        pass
                    break

    def search_assist(self, block_list, robot_list):
        found=False
        for rover in robot_list:
            if rover.resource_sharing == True and rover.carry == False:
                for polygon in block_list:
                    if ((-60 < (self.pos[0] - polygon.rect.center[0]) < 60 and -60 < (
                            self.pos[1] - polygon.rect.center[1]) < 60) or polygon.robo == self.id):
                        if rover.capable_available['RA']==1:
                            if polygon.robo == 'R0':
                                rover.destination = polygon.rect.center
                                found=True
                                break
                        if found == True:
                            return

    def camera_assist(self):
        try:
            self.color = self.camera.identify_color(self)
            self.shape = self.camera.identify_shape(self)
            self.destination = self.green.get_rack_location(self.color, self.shape)

        except:
            pass

    def smart_collision(self,robot_list):
        # -- Rotation Direction
        if self.Smart_collision==False:
            self.direction = 0
            while self.direction == 0:
                self.direction = random.randint(-1,1)
        # -- Movement base on direction
        self.Smart_collision=True
        self.rover_heading_callibrate()
        self.prev_pos=self.pos
        self.movement_forward()
        self.movement_forward()
        self.pos_update()
        collision = self.robot_collide(robot_list)
        if collision == 1:
            self.body_rotate(self.direction)
            self.pos=self.prev_pos
            #self.collision=1
        else:
            prev=self.pos

            # -- Advance Collision Check
            self.Queue = self.path_p.create_path(self.destination)
            collision =0
            for i in range (0,50):
                print(self.id,"Collision check enterd!!!!!!!!!!")
                try:
                    self.Queue.pop(0)
                    self.pos = self.Queue.pop(0)
                except:
                    pass
                # -- Recheck Collision
                collision = self.robot_collide(robot_list)
                if collision == 1:
                    break

            self.pos = prev
            self.prev_pos=self.pos
            if collision == 0:
                self.Smart_collision=False
            else:
                self.pos=self.prev_pos


    def rover_heading_callibrate(self):
        # -- Rover heading calibration
        if self.rover_heading < 0:
            self.rover_heading += 360
        if self.rover_heading > 359:
            self.rover_heading -= 360

    def pos_update(self):
        self.rover_rect.center=self.pos
        self.rover_rect.center = [self.size[0] / 2, self.size[1] / 2]
        self.arm_rect.center = self.rover_rect.center
        self.arm_up_rect.center = [self.arm_rect.center[0] + self.arm_up_offset * math.cos(
            (self.arm_heading + self.rover_heading) * math.pi / 180.0),
                                   self.arm_rect.center[1] + self.arm_up_offset * math.sin(
                                       -(self.arm_heading + self.rover_heading) * math.pi / 180.0)]

    def movement_forward(self):
        self.pos=list(self.pos)

        Heading=(self.rover_heading)
        if 0 <= Heading < 23 or 338 < Heading < 360:
            self.pos[0] += 1
            self.pos[1] += 0
        elif 22 < Heading < 68:
            self.pos[0] += 1
            self.pos[1] -= 1
        elif 67 < Heading < 113:
            self.pos[0] += 0
            self.pos[1] -= 1
        elif 112 < Heading < 158:
            self.pos[0] -= 1
            self.pos[1] -= 1
        elif 157 < Heading < 203:
            self.pos[0] -= 1
            self.pos[1] += 0
        elif 202 < Heading < 248:
            self.pos[0] -= 1
            self.pos[1] += 1
        elif 247 < Heading < 293:
            self.pos[0] += 0
            self.pos[1] += 1

        elif 292 < Heading < 339:
            self.pos[0] += 1
            self.pos[1] += 1
        self.rect.center = self.pos
        self.rover_rect.center = [self.size[0] / 2, self.size[1] / 2]
        self.arm_rect.center = self.rover_rect.center
        self.arm_up_rect.center = [self.arm_rect.center[0] + self.arm_up_offset * math.cos(
            (self.arm_heading + self.rover_heading) * math.pi / 180.0),
                                   self.arm_rect.center[1] + self.arm_up_offset * math.sin(
                                       -(self.arm_heading + self.rover_heading) * math.pi / 180.0)]

pygame.quit()
