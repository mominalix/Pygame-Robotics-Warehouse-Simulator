import pygame

" !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  Rack Class !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"


class rack(pygame.sprite.Sprite):
    def __init__(self, rack_id):
        self.rack_id =rack_id
        self.shape_count = 0
        self.red_square=(1190,144)
        self.red_pentagon=(1190,179)
        self.red_triangle=(1190,118)
        self.green_square = (600, 144)
        self.green_pentagon = (600, 179)
        self.green_triangle = (600, 118)
        self.blue_square = (885, 144)
        self.blue_pentagon = (885, 179)
        self.blue_triangle = (885, 118)

    def add_shape(self):
        #print("add_shape called")
        self.shape_count+=1
        return

    def get_rack_location(self,color,shape):
        if color == "red":
            if shape == "square":
                return self.red_square
            elif shape == "pentagon":
                return self.red_pentagon
            elif shape == "triangle":
                return self.red_triangle
        elif color == "green":
            if shape == "square":
                return self.green_square
            elif shape == "pentagon":
                return self.green_pentagon
            elif shape == "triangle":
                return self.green_triangle
        elif color == "blue":
            if shape == "square":
                return self.blue_square
            elif shape == "pentagon":
                return self.blue_pentagon
            elif shape == "triangle":
                return self.blue_triangle
        else:
            print("False Return")
            return (0,0)