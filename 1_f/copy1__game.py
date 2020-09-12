import pygame

# from pygame import display
import neat
import os
import random
import time

pygame.font.init()
# os.environ['SDL_VIDEODRIVER']='windlib'
# os.environ['SDL_VIDEODRIVER']='windlib'
# os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.display.list_modes()



WIN_WIDTH=500
WIN_HEIGHT=800

BIRD_IMGS=[pygame.transform.scale2x(pygame.image.load(os.path.join("../imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("../imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("../imgs","bird3.png")))]
PIP_IMG=pygame.transform.scale2x(pygame.image.load(os.path.join("../imgs","pipe.png")))
BASE_IMG=pygame.transform.scale2x(pygame.image.load(os.path.join("../imgs","base.png")))
BG_IMG=pygame.transform.scale2x(pygame.image.load(os.path.join("../imgs","bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans",50)

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

    def jump(self):
        self.vel = -10.5
        self.tick_count= 0
        self.height = self.y

    def move(self):
        self.tick_count +=1

        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        if d >= 16:
            d = 16

        if d < 0:
            d -= 2

        self.y = self.y +d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt=self.MAX_ROTATION
        else:
            if self.tilt> -90:
                self.tilt -=self.ROT_VEL


    def draw(self, win):
        self.img_count +=1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME *2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME *3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME *4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME *4 +1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image= pygame.transform.rotate(self.img,self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x,self.y)).center)
        win.blit(rotated_image,new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP=200
    VEL=5 

    def __init__(self,x):
        self.x=x
        self.height = 0
        # self.gap =100

        self.top=0
        self.bottom=0
        self.PIP_TOP=pygame.transform.flip(PIP_IMG,False, True)
        self.PIP_BOTTOM =PIP_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIP_TOP.get_height()
        self.bottom=self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIP_TOP,(self.x,self.top))
        win.blit(self.PIP_BOTTOM,(self.x,self.bottom))

    def collide(self, bird ):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIP_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIP_BOTTOM)

        top_offset    = (self.x -bird.x, self.top - round(bird.y))
        bottom_offset = self.x - bird.x, self.bottom - round(bird.y)

        b_point = bird_mask.overlap(bottom_mask,bottom_offset) # bottom point

        t_point = bird_mask.overlap(top_mask,top_offset) # top point

        # check for collision
        if t_point or b_point:
            return True
        else:
            return False



class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self,y):
        self.y=y
        self.x1 =0
        self.x2 =self.WIDTH

    def move(self):
        self.x1 -=self.VEL
        self.x2 -=self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 +self.WIDTH

        if self.x2 +self.WIDTH <0:
            self.x2= self.x1 +self.WIDTH

    def draw(self,win):
        win.blit(self.IMG,(self.x1,self.y))
        win.blit(self.IMG,(self.x2,self.y))










def draw_window(win,birds,pipes,base,score):

    # screen = pygame.display.set_mode((400, 300))
    # pygame.draw.circle(screen, (0,0,0), (25,25),25)
    # print("dvdgd")


    win.blit(BG_IMG, (0,0))
    for pipe in pipes:
        print("Here is pipes")
        pipe.draw(win)

    text = STAT_FONT.render("Score" + str(score),1,(255,255,255))
    win.blit(text,(WIN_WIDTH - 10 -text.get_width(),10))

    base.draw(win)
    for bird in birds:
        bird.draw(win)
    pygame.display.update()

# eval_genome, fitness function
def main(genomes,config):
    # bird = Bird(230,350)
    nets = []
    ge =[]
    birds = []


    # g is tuple ( 1, ge)
    # _,g is to get onlt the object
    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        birds.append(Bird(230,350))
        g.fitness = 0
        ge.append(g)
    base=Base(730)
    pipes=[Pipe(600)]

    # print("mnmnmn")
    # try:
    #     os.environ["DISPLAY"]
    # except:
    #     os.environ["SDL_VIDEODRIVER"] = "dummy"
    win=pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    clock=pygame.time.Clock()

    score =0
    run =True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        # bird.move()

        # - if there are more than pipe * NOT SURE * 
        pipe_ind= 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds [0].x > pipes[0].x + pipes[0].PIP_TOP.get_width():
                pipe_ind = 1
        else:
            run =False
            break

        for x,bird in enumerate(birds):
            bird.move()
            ge[x].fitness +=0.1

            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height),abs(bird.y -pipes[pipe_ind].bottom)))
            if output[0] > 0.5 :
                bird.jump()
        add_pipe= False
        rem=[]
        for pipe in pipes:

            for x,bird in enumerate(birds):
                ge[x].fitness -=1
                # birds.remove(bird)
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)


                if pipe.collide(bird):
                    pass

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed= True
                    add_pipe = True
            if pipe.x + pipe.PIP_TOP.get_width() <0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score +=1
            for g in ge:
                g.fitness +=5
            pipes.append(Pipe(600))

        for r in rem :
            pipes.remove(r)
        
        for x,bird in enumerate(birds):

            if bird.y +bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)


        base.move()
        draw_window(win,birds,pipes, base,score)

        # print("kjkjkjkjk")


    


def run(config_path):

    # load Configuration file
    config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)

    # Set population
    p=neat.Population(config)

    # set the input we are going to see
    p.add_reporter(neat.StdOutReporter(True))
    stats=neat.StatisticsReporter()
    p.add_reporter(stats)

    # set the fitness function that we are going to run to 50 generations
    # It will call main function 50 times
    winner = p.run(main,50)

    




# def main():
#     bird = Bird(230,350)
#     base=Base(730)
#     pipes=[Pipe(600)]

#     # print("mnmnmn")
#     # try:
#     #     os.environ["DISPLAY"]
#     # except:
#     #     os.environ["SDL_VIDEODRIVER"] = "dummy"
#     win=pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
#     clock=pygame.time.Clock()

#     score =0
#     run =True
#     while run:
#         clock.tick(30)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#         # bird.move()
#         add_pipe= False
#         rem=[]
#         for pipe in pipes:
#             if pipe.collide(bird):
#                 pass

#             if pipe.x + pipe.PIP_TOP.get_width() <0:
#                 rem.append(pipe)

#             if not pipe.passed and pipe.x < bird.x:
#                 pipe.passed= True
#                 add_pipe = True
#             pipe.move()
#         if add_pipe:
#             score +=1
#             pipes.append(Pipe(600))

#         for r in rem :
#             pipes.remove(r)
        
#         if bird.y +bird.img.get_height() >= 730:
#             pass


#         base.move()
#         draw_window(win,bird,pipes, base,score)

#         # print("kjkjkjkjk")


#     pygame.quit()
#     quit()

if __name__ == "__main__":
    # import pygame
    # import os
    # os.environ["SDL_VIDEODRIVER"] = "dummy"
    """
    This from PYCHARM
    """


    # pygame.init()
    # pygame.display.list_modes()
    # print("mmmmmmmmmmmmm")
    # main()
    local_dir= os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config_feedforward.txt")
    run(config_path)
    # main()

    # print("THIS FROM PYCHARMA")
    # from pygame.locals import *
    # screen = pygame.display.set_mode((400, 300))
    # pygame.draw.circle(screen, (0,0,0), (25,25),25)



