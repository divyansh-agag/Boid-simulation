
import pygame as pg
import sys
import math
import random
import numpy as np
pg.init()
width=1000
height=800
screen = pg.display.set_mode((width, height))
clock = pg.time.Clock()

Particles=[]
particle_radi=2
vision=40
velocity=2
class Particle:
    def __init__(self,pos,vel,is_gen,id):#paricle initialization#
        self.pos=pos
        self.id=id#
        self.vel=vel#0 idx for x , 1 idx for y
        self.is_gen=is_gen
        self.clr=(0,100,200)
        if(self.is_gen):self.clr=(200,0,50)
        self.radi=particle_radi
        self.vision_dist = vision
        self.curr_velocity_angle=math.atan2(self.vel[1], self.vel[0])
        Particles.append(self)
        self.nudge=0#
    def compute_nears(self):
        near_particles=[]
        for particle in Particles:
            if particle == self:continue
            dist = math.hypot(self.pos[0]-particle.pos[0], self.pos[1]-particle.pos[1])
            if(dist< vision ):near_particles.append(particle)
        return near_particles
    def compute_nudge(self,near_particles):
        nudge=0
        nudge_constant=0.02#more means more responsive
        for near_particle in near_particles:
            dist_vector=[near_particle.pos[0]-self.pos[0], near_particle.pos[1]-self.pos[1]]
            dist_vector_angle = math.atan2(dist_vector[1], dist_vector[0])#in rads
            dist_vector_angle*=-1
            dist_vector_angle+=math.pi/2
            if(dist_vector_angle>math.pi):dist_vector_angle-=2*math.pi
            diff = dist_vector_angle - self.curr_velocity_angle#
            diff=((diff+math.pi)%(2*math.pi))-math.pi
            nudge+=nudge_constant/diff
        nudge_cap=0.1
        if (nudge>nudge_cap):nudge=nudge_cap#cap the angular vel to 3 deg per frame
        if(nudge<-nudge_cap):nudge=-nudge_cap
        self.nudge=nudge#
        return nudge
    def compute_avg_near_dirc(self, nears):
        if not nears:
                return -1
        sx, sy = 0, 0
        for near in nears:
            sx += math.cos(near.curr_velocity_angle)
            sy += math.sin(near.curr_velocity_angle)
        return math.atan2(sy, sx)
    
    def update_vel_avg(self):
        nears=self.compute_nears()
        avg_dirc=self.compute_avg_near_dirc(nears)
        if avg_dirc!=-1:
            diff=avg_dirc-self.curr_velocity_angle
            diff=((diff+math.pi)%(2*math.pi))-math.pi
            avg_vel_constant=0.1
            nudge=diff*avg_vel_constant
            new_velocity_angle=self.curr_velocity_angle+nudge
            self.vel[0]=velocity*math.cos(new_velocity_angle)
            self.vel[1]=velocity*math.sin(new_velocity_angle)
            self.curr_velocity_angle=new_velocity_angle
    def update_vel_coll(self):
        nears=self.compute_nears()
        nudge=self.compute_nudge(nears)
        new_velocity_angle=self.curr_velocity_angle-nudge
        self.vel[0]=velocity*math.cos(new_velocity_angle)
        self.vel[1]=velocity*math.sin(new_velocity_angle)
        self.curr_velocity_angle=new_velocity_angle
    def update(self):
        #self.update_vel_coll()
        self.update_vel_avg()
        self.pos[0]+=self.vel[0]
        self.pos[1]+=self.vel[1]
        if(self.pos[0]> width):
            self.pos[0]-=width
        if(self.pos[0]< 0):
            self.pos[0]+=width
        if(self.pos[1]> height):
            self.pos[1]-=height
        if(self.pos[1]< 0):
            self.pos[1]+=height
    def draw(self,screen):
        pg.draw.circle(screen, self.clr, self.pos, self.radi)
        #pg.draw.circle(screen, (0,125,200), self.pos, self.vision_dist,1 )
        constant=20/velocity
        pg.draw.line(screen,self.clr, self.pos, (self.vel[0]*constant+self.pos[0], self.vel[1]*constant+ self.pos[1]))

particle_count=400
for i in range(0,particle_count):
    angle = random.uniform(0, 2 * math.pi)
    vel = [velocity * math.cos(angle), velocity * math.sin(angle)]
    par = Particle([random.randint(0, width), random.randint(0, height)], vel,0, id=i)#

count=particle_count#
def inp_handel():
    global count
    mouse_pos=pg.mouse.get_pos()
    for e in pg.event.get():
        if e.type == pg.QUIT: pg.quit(); sys.exit()
        if(e.type == pg.MOUSEBUTTONDOWN):
            angle = random.uniform(0, 2 * math.pi)
            vel = [velocity * math.cos(angle), velocity * math.sin(angle)]
            par = Particle(list(mouse_pos),vel,1, id=count)#
            count+=1
while True:
    inp_handel()
    screen.fill((0, 0, 0))
    for particle in Particles:
        particle.update()
        particle.draw(screen)
    pg.display.flip()
    clock.tick(30)