"""
This file handles the vehicles, including how they drive, where they want to go, where they can go and will go.
"""
from map_handler import map
from random import choice
import pathfinder as path
from tiles import width as tw
from surface_handler import screen_size, scaled_map, minimap
import pygame
from time import time
from os import listdir

# the car class
class car:
    # update timer for the movement
    next_tick = 0
    
    # function to generate n cars
    def generate(amount):
        for _ in range(amount): vehicles.append(car())
        
    # function to update and blit all vehicles
    def update_all(target):
        if time() > car.next_tick:
            for i in vehicles:
                i.drive()
            car.next_tick = time() + 0.02
        for i in vehicles:
            i.show(target)
    
    # function to turn the vehicle based on the upcoming path
    def find_direction_based_on_next_tile(self):
        next_pos = self.path[0]
        if next_pos[0] == self.current_tile[0]:
            if next_pos[1] < self.current_tile[1]: #N
                self.dir = 0
                self.position_on_tile = (tw*0.75, tw)
            else: #S
                self.dir = 180
                self.position_on_tile = (tw/4, 0)
        else:
            if next_pos[0] > self.current_tile[0]: #E
                self.dir = 90
                self.position_on_tile = (0, tw*0.75)
            else: #W
                self.dir = 270
                self.position_on_tile = (tw, tw/4)
    
    # function to turn the vehicle based on the current tile
    def find_direction_based_on_positions_on_tile(self):
        next_pos  = self.steps_on_tile[0]
        match next_pos:
            case (-1,0): self.dir = 270 #N
            case (0,1): self.dir = 180 #E
            case (1,0): self.dir = 90 #S
            case (0,-1): self.dir = 0 #W
            
    # function to initialize a new car
    def __init__(self, tile=None, goal = None):
        if tile is None: self.current_tile = choice(list(map.street_positions))
        else: self.current_tile = tile
        if goal is None: self.goal = choice(list(map.street_positions))
        else: self.goal = goal
        self.path = path.find(self.current_tile, self.goal)
        self.speed = 1
        self.position_on_tile = (0,0)
        self.steps_on_tile = []
        self.dir = 0
        self.find_direction_based_on_next_tile()
        img = pygame.image.load("car_sprites/"+choice(listdir("car_sprites")))
        
        self.images = {}
        for i in scaled_map.zoom_steps: self.images[str(i)] = pygame.transform.smoothscale(img, (int(i/1.5), int(i/3)))
    
    # find the steps on the current tile
    def find_steps_on_tile(self):
        n1 = self.current_tile
        if len(self.path) > 1:
            n2 = self.path[0]
            if self.dir == 0: #N
                if n1[0] == n2[0]: self.steps_on_tile = [(0,-1)]*8
                elif n1[0] > n2[0]: self.steps_on_tile = [(0,-1)]*6 + [(-1,0)]*6
                else: self.steps_on_tile = [(0,-1)]*2+[(1,0)]*2
            elif self.dir == 90: #E
                if n1[1] == n2[1]: self.steps_on_tile = [(1,0)]*8
                elif n1[1] > n2[1]: self.steps_on_tile = [(1,0)]*6+[(0,-1)]*6
                else: self.steps_on_tile = [(1,0)]*2+[(0,1)]*2
            elif self.dir == 180: #S
                if n1[0] == n2[0]: self.steps_on_tile = [(0,1)]*8
                elif n1[0] < n2[0]: self.steps_on_tile = [(0,1)]*6 + [(1,0)]*6
                else: self.steps_on_tile = [(0,1)]*2+[(-1,0)]*2
            else: #W
                if n1[1] == n2[1]: self.steps_on_tile = [(-1,0)]*8
                elif n1[1] < n2[1]: self.steps_on_tile = [(-1,0)]*6+[(0,1)]*6
                else: self.steps_on_tile = [(-1,0)]*2+[(0,-1)]*2
        else:
            if self.dir == 0: self.steps_on_tile = [(0,-1)]*8 #N
            elif self.dir == 90: self.steps_on_tile = [(1,0)]*8 #E
            elif self.dir == 180: self.steps_on_tile = [(0,1)]*8 #S
            else: self.steps_on_tile = [(-1,0)]*8 #W
    
    # find a new goal for the car
    def new_goal(self): 
        while self.goal == self.current_tile:
            self.goal = choice(list(map.street_positions))
        self.path = path.find(self.current_tile, self.goal)
    
    # update the position
    def drive(self):        
        if len(self.steps_on_tile) == 0:
            self.find_direction_based_on_next_tile()
            self.current_tile = self.path.pop(0)
            if self.current_tile == self.goal: 
                self.new_goal()
                self.path.pop(0)
            self.find_steps_on_tile()
            
            

        else: self.find_direction_based_on_positions_on_tile()
        move = self.steps_on_tile.pop(0)  
        new_x = tw/8 * move[0] + self.position_on_tile[0]
        new_y = tw/8 * move[1] + self.position_on_tile[1]
        self.position_on_tile = (new_x, new_y)       

    # blit the cars on the corresponding position
    def show(self, target:pygame.Surface):
        img = pygame.transform.rotate(self.images[str(scaled_map.zoom)], 90 - self.dir)
        screen_x = int(scaled_map.pos[0] + self.current_tile[0]*scaled_map.zoom + scaled_map.zoom/tw * self.position_on_tile[0] - img.get_width()/2)
        screen_y = int(scaled_map.pos[1] + self.current_tile[1]*scaled_map.zoom + scaled_map.zoom/tw * self.position_on_tile[1] - img.get_height()/2)
        if -50 < screen_x < screen_size()[0] + 50 and -50 < screen_y < screen_size()[1] + 50:
            target.blit(img, (screen_x,screen_y))
        """#uncomment to see the goals
        screen_x = int(scaled_map.pos[0] + self.goal[0]*scaled_map.zoom)
        screen_y = int(scaled_map.pos[1] + self.goal[1]*scaled_map.zoom)
        if -50 < screen_x < screen_size()[0] + 50 and -50 < screen_y < screen_size()[1] + 50:
            pygame.draw.rect(target, (255,0,0), (screen_x,screen_y,scaled_map.zoom,scaled_map.zoom))
        """
        
    # blit the positions of the cars to the minimap
    def blit_on_minimap():
        r = max(1, int((minimap.s.get_width()/map.width)/2))
        for v in vehicles:
            px = int(minimap.s.get_width()*(v.current_tile[0]/map.width) + v.position_on_tile[0]/tw*(minimap.s.get_width()/map.width))
            py = int(minimap.s.get_height()*(v.current_tile[1]/map.height)+ v.position_on_tile[1]/tw*(minimap.s.get_height()/map.height))
            #minimap.s.set_at((px,py), (255,0,0))
            pygame.draw.circle(minimap.s, (255,0,0), (px,py), r, 1)

# the list of all cars on the map
vehicles:list[car] = []