import pygame
import pymunk
import random
import matplotlib.pyplot as plt
from pymunk import shapes
import numpy as np
pygame.init()
display =pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
space = pymunk.Space()
FPS= 90
pop = 300
recovery_period = 300

class Ball():
    def __init__(self,x,y):
        self.x = x
        self.y= y
        self.infected = False
        self.recovered = False
        self.infected_time = 0
        self.susceptible = False 
        self.body = pymunk.Body()
        self.body.position = x,y
        self.body.velocity = random.uniform(-100,100),random.uniform(-100,100)
        self.shape = pymunk.Circle(self.body,10)
        self.shape.density = 1
        self.shape.elasticity = 1
        self.distance = False
        space.add(self.body,self.shape)

    def infect(self,space=0,arbiter=0,data=0):
        self.infected = True  
        self.shape.collision_type = pop+1 
        if(self.distance):
            self.body.velocity = self.body.velocity/8
            self.shape.density = 10000
        
    def pass_time(self):
        if self.infected:
            self.infected_time += 1
        if self.infected_time >= recovery_period:
            self.infected = False
            self.recovered = True
            self.distance = False
            self.susceptible = False
            self.shape.collision_type =  pop+3

    def draw(self):
        x,y = self.body.position
        if self.infected:
            pygame.draw.circle(display,(255,0,0),(int(x),int(y)),10)
            self.distance= random.choice([True,False])
        elif self.recovered:
            self.distance =False
            self.body.velocity = random.uniform(-100,100),random.uniform(-100,100)
            self.shape.density = 1
            pygame.draw.circle(display,(128,128,128),(int(x),int(y)),10)
           
        else:
            pygame.draw.circle(display,(63,244,208),(int(x),int(y)),10)
class Wall():
    def __init__(self, p1, p2):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, p1, p2, 5)
        self.shape.elasticity =1
        space.add(self.body,self.shape)
infected_count = []
def game():
    balls = [Ball(random.randint(0,800),random.randint(0,800)) for i in range(pop)]
    for i in range(len(balls)):
     #   balls[i].distance= random.choice([True,False])
        balls[i].susceptible = random.choices([True,False],weights=(70,30),k=1)
    for i in range(1,pop+1):
        balls[i-1].shape.collision_type = i
        handler = space.add_collision_handler(i,pop+1) 
        handler.separate = balls[i-1].infect

    walls = [Wall((0,0),(0,800)),
             Wall((0,0),(800,0)),
             Wall((0,800),(800,800)),
             Wall((800,0),(800,800))]
    random.choice(balls).infect()
    
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            
        display.fill((0,0,0))
        infected_count_i = 0
        for ball in balls:
            ball.draw()
            ball.pass_time()
            if ball.infected: 
                infected_count_i +=1
        if len(infected_count) <= 1000:
            infected_count.append(infected_count_i)
        pygame.display.update()
        clock.tick(FPS)
        space.step(1/FPS)
        
game()
x = np.arange(0, len(infected_count), 1)
fig, ax = plt.subplots()
ax.plot(x, infected_count)
ax.set(xlabel='x', ylabel='infection couunt',
       title='Covid Simulation')
ax.grid()
plt.show()
pygame.quit()
