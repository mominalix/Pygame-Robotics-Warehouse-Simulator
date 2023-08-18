import pygame
import pygame.freetype

###### COLOUR DEFINATIONS ######
BLACK = (0, 0, 0, 0)
WHITE = (255, 255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 255, 255)
" !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  Server Class !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
class server(pygame.sprite.Sprite):
    def __init__(self,screen):
        self.resource_sharing=1
        self.n_processes=1
        self.img_addr = './data/'
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([91, 56]).convert_alpha()
        self.image.fill(WHITE)
        self.obj =  pygame.image.load(self.img_addr+"server.png").convert_alpha()
        self.image.blit(self.obj, [0, 0])
        self.rect = self.image.get_rect()
        self.rect.center =[1450,80]
        self.LED=1
        self.screen=screen
        self.text_call = 1
        self.largeText = pygame.font.SysFont('Calibri', 16)

    def blink(self):
        if self.LED ==1:
            self.img_addr = './data/'
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface([5, 5]).convert_alpha()
            self.image.fill(WHITE)
            self.obj = pygame.image.load(self.img_addr + "led.png").convert_alpha()
            self.image.blit(self.obj, [0, 0])
            self.rect = self.image.get_rect()
            self.rect.center = [1471, 81]
            self.LED=0
        else:
            self.img_addr = './data/'
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface([5, 5]).convert_alpha()
            self.image.fill(WHITE)
            self.obj = pygame.image.load(self.img_addr + "led_off.png").convert_alpha()
            self.image.blit(self.obj, [0, 0])
            self.rect = self.image.get_rect()
            self.rect.center = [1471, 81]
            self.LED = 1

    def identify_polygon(self):
        return

    def nearest_rover(self):
        print("nearest_rover called")
        return

    def assign_priority(self):
        print("assign_prioirity called")
        return

    def bypass_process(self):
        print("bypass_process called")
        return

    def text_objects(self,text, font):
        textSurface = font.render(text, True, (0,76,112))
        return textSurface, textSurface.get_rect()

    def message_display(self,text):
        if self.text_call < 2:
            pygame.sprite.Sprite.__init__(self)
        TextSurf, TextRect = self.text_objects(text, self.largeText)
        TextRect.center = [1450, 120]
        self.screen.blit(TextSurf, TextRect)
        self.text_call+=1