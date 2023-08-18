import pygame

" !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  camera_module Class !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
class camera_module(pygame.sprite.Sprite):
    def __init__(self):
        self.camera = True

    def identify_color(self,robot):
        return robot.polygon.Color

    def identify_shape(self,robot):
        return robot.polygon.shape