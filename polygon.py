import pygame
import random
from math import sin, cos, radians, pi

###### COLOUR DEFINATIONS ######
BLACK = (0, 0, 0, 0)
WHITE = (255, 255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 255, 255)

" !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  Polygon Class !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"


class polygon(pygame.sprite.Sprite):
    """
    This class represents the polygon.
    It derives from the "Sprite" class in Pygame.
    """

    def __init__(self,polygon_id,coordinates):
        """ Constructor. Pass in the color of the block,
        and its size. """
        self.pick = False
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.polygon_id = polygon_id
        # self.polygon_id = random.choice(
        #     ['red_pentagon', 'red_square', 'red_triangle', 'green_triangle', 'green_pentagon', 'green_square',
        #      'blue_triangle', 'blue_pentagon', 'blue_square'])
        self.id = self.polygon_id
        self.color = self.polygon_id[0]
        word = self.polygon_id.split("_")
        self.Color = word[0]
        self.shape = word[1]
        self.image = pygame.Surface([46, 43]).convert_alpha()
        self.image.fill(WHITE)
        self.img_addr = './data/'
        self.obj = pygame.image.load(self.img_addr + self.polygon_id + ".png").convert_alpha()
        self.image.blit(self.obj, [0, 0])
        self.coordinates=coordinates
        #self.coordinates = (random.randint(400, 1500), random.randint(400, 800))
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.center = self.coordinates
        self.placed = 0
        self.robo = 'R0'
        self.priority = 0
        if self.color[0] == 'r':
            self.priority += 3
        elif self.color[0] == 'b':
            self.priority += 2
        elif self.color[0] == 'g':
            self.priority += 1
        if self.shape[0] == 't':
            self.priority += 1
        elif self.shape[0] == 's':
            self.priority += 2
        elif self.shape[0] == 'p':
            self.priority += 3

    def update_position(self, robot_list):
        # print("print_position called")
        if self.pick == True:
            for robot in robot_list:
                if robot.id == self.robo:
                    self.robot = robot
                    x1 = self.robot.pos[0]
                    y1 = self.robot.pos[1]
                    angle = self.robot.arm_heading + self.robot.rover_heading +90
                    angle=self.angle_callibrate(angle)
                    self.rect.center = self.point_pos(x1, y1, 45 + self.robot.arm_up_offset, angle)

    def point_pos(self, x0, y0, d, theta):
        theta_rad = pi / 2 - radians(theta)
        return x0 + d * cos(theta_rad), y0 + d * sin(theta_rad)

    def angle_callibrate(self,angle):
        if angle< 0:
            angle += 360
        if angle > 359:
            angle -= 360
        return angle
