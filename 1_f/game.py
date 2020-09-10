import pygame
import neat
import os
import random
import time

WIN_WIDTH=600
WIN_HEIGHT=800

BIRD_IMGS=[pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
PIP_LINE=pygame.transform.scale2x(pygame.img.load(os.path.join("imgs","pipe.png")))
BASE_LINE=pygame.transform.scale2x(pygame.img.load(os.path.join("imgs","base.png")))
BG_LINE=pygame.transform.scale2x(pygame.img.load(os.path.join("imgs","bg.png")))


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
