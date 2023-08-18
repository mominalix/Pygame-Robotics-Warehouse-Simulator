import pygame
import math
import random

" !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  path_planning Class !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
class path_plannig(pygame.sprite.Sprite):
    def __init__(self, robot, pos):
        self.path_planner = True
        self.r = robot
        self.Queue = []
    def plan_path(self):
        destination = (random.randint(420, 1525), random.randint(370, 825))
        return destination

    def create_path(self, target):
        queue = []
        ax = self.r.pos[0]
        ay = self.r.pos[1]
        bx = target[0]
        by = target[1]
        steps_number = max(abs(bx - ax), abs(by - ay))
        try:
            stepx = float(bx - ax) / steps_number
            stepy = float(by - ay) / steps_number
        except:
            pass
        for i in range(steps_number + 1):
            queue.append((int(ax + stepx * i), int(ay + stepy * i)))
        return queue

    def polygon_search(self):
        print("polygon_search")
        return