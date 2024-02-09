import pygame
import event_handler
from map_handler import map

# Initialise the pygame modules
pygame.init()

##############################################
####### Load the map you want to load ########
####### Maximal map size: 200 x 200 px #######
######### The map has to be a square. ########
map.load("maps/bad_mergentheim.png")
##############################################

# Set up the Window
screen = pygame.display.set_mode()
pygame.display.update()
sw,sh = screen.get_size()

# had to move this import as that file needs an open window
import surface_handler as surf


# set up the surfaces
surf.init()

# read the map
surf.loading_surface.update(screen, "Loading map")
map.read_image()
map.blit_map_to(surf.original_map.s)
# blit the tiles for the first time
surf.loading_surface.update(screen, progressbar=True)
surf.scaled_map.load_cache(screen)
surf.scaled_map.init()
surf.loading_surface.update(screen, "Almost there")
# initialise the minimap
surf.minimap.init()

# main loop
while True:
    # handle events
    event_handler.main()
    
    # empty the surfaces
    surf.clear()
    
    # set the background of the window
    screen.fill((234,227,204))
    
    # update and blit stuff of the main map and the minimap
    surf.main.update_map()
    surf.minimap.update()
    # blith the other surfaces
    for s in range(4): screen.blit(surf.all[s].s, surf.all[s].pos)
    
    # update window
    pygame.display.flip()
