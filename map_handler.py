"""
This file contains nearly all variables and functions to make the analysis of the map work properly.
The tasks go from openinig and reading the map to analyzing intersectionssections to plotting the translated map on a pygame surface.
"""

import pygame
import tiles

# class to manage all the important stuff
class map:
    # define the required variables
    width, height = size = (0,0)
    tiles = set()
    source_str = ""
    img = pygame.Surface((0,0))
    pixel_array = ()
    
    # function to load the map from a image
    def load(source: str):
        map.source_str = source
        map.img = pygame.image.load(source)
        map.width, map.height = map.size = map.img.get_size()

        pixels = []
        for x in range(map.width):
            for y in range(map.height):
                pixels.append(map.img.get_at((x,y)))
        map.pixel_array = tuple(pixels)
        map.street_positions = set()
    
    # function to find the tiles surrounding a specific tile, returning a tuple (N,E,S,W)
    def get_surrounding_tiles(pos): 
        x,y = pos
        tiles = [0,0,0,0]
        if y>0: tiles[0] = map.img.get_at((x,y-1))
        if x<map.width-1: tiles[1] = map.img.get_at((x+1,y))
        if y<map.height-1: tiles[2] = map.img.get_at((x,y+1))
        if x>0: tiles[3] = map.img.get_at((x-1,y))
        return tiles
    
    # function to analize the source image and detect the different tiles
    def read_image():
        for x in range(map.width):
            for y in range(map.height):
                p = map.img.get_at((x,y))
                surrounding = map.get_surrounding_tiles((x,y))
                
                # streets
                if p == (0,0,0):
                    
                    # check for surrounding street tiles to calculate the correct image
                    intersections = [0,0,0,0]
                    for i in range(len(surrounding)):
                        if surrounding[i] == (0,0,0,255): intersections[i] = 1
                    map.tiles.add(tiles.street(intersections, (x*tiles.width,y*tiles.width)))
                    map.street_positions.add((x,y))
                    
                # buildings
                if p == (0,255,0):
                    
                    # if this is the top - left - corner of the house, measure the size and append it to the map
                    if surrounding[0] != (0,255,0) and surrounding[3] != (0,255,0):
                        w = 1
                        h = 1
                        tempx = x
                        tempy = y
                        
                        # calculate the size of the building
                        while map.get_surrounding_tiles((tempx,y))[1] == (0,255,0):
                            w += 1
                            tempx += 1
                        while map.get_surrounding_tiles((x,tempy))[2] == (0,255,0):
                            h += 1
                            tempy += 1
                        map.tiles.add(tiles.building((w,h), (x*tiles.width,y*tiles.width)))
    
    # function to blit the tiles to a surface
    def blit_map_to(target_surface):
        target_surface.fill((234,227,204))
        for t in map.tiles: t.blit(target_surface)               
