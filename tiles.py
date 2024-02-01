"""
This file contains nearly all information concerning the tiles.
Tiles refers to all the objects in the background, such as streets an buildings.
"""

import pygame
from random import choice
from os import listdir

# define tilesize
width, height = size = (50,50)

# parent class for the tiles with functions affecting all types of tiles
class tile:
    img = pygame.Surface(size)
    
    def __init__(self, img, pos):
        self.img = img
        self.pos = pos
        
    def blit(self, surf):
        surf.blit(self.img, self.pos)
        

# class for the street - tiles
class street(tile):
    # load the different images for different types of road
    img_straight = pygame.image.load("tiles/street_straight.png")
    img_corner = pygame.image.load("tiles/street_corner.png")
    img_intersect3 = pygame.image.load("tiles/street_intersect3.png")
    img_intersect4 = pygame.image.load("tiles/street_intersect4.png")
    
    def __init__(self, intersections, pos):
        # detect the type of street tile to use
        if sum(intersections) == 2:
            if intersections == [1,0,1,0]: img = pygame.transform.rotate(street.img_straight,90.)
            elif intersections == [0,1,0,1]: img = street.img_straight
            else:
                if intersections == [1,0,0,1]: img = street.img_corner
                else: img = pygame.transform.rotate(street.img_corner, (3-intersections.index(1))*90.)
        elif sum(intersections) == 3:
            img = pygame.transform.rotate(street.img_intersect3, (2-intersections.index(0))*90.)
        else: img = street.img_intersect4
        super().__init__(img, pos)
        

# class for the different buildings
class building(tile): 
    # load the different buildings of different sizes
    b_2x2 = (list(pygame.image.load("tiles/buildings/2x2/"+i) for i in listdir("tiles/buildings/2x2")))
    b_2x3 = (list(pygame.image.load("tiles/buildings/2x3/"+i) for i in listdir("tiles/buildings/2x3")))
    b_3x2 = (list(pygame.image.load("tiles/buildings/3x2/"+i) for i in listdir("tiles/buildings/3x2")))
    
    def __init__(self, size, pos):
        #decide the image for the building according to it´s size
        if size == (2,3): img = choice(building.b_2x3)
        elif size == (3,2): img = choice(building.b_3x2)
        else: img = choice(building.b_2x2)
        super().__init__(img, pos)