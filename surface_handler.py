"""
This file manages the different surfaces on the screen, including
- the "main"-surface containing everything shown (just an extra layer to the window surface)
- the "stats"-surface containing some statistics
- the "controll"-surface showing the inputs the user is able to perform
- the "minimap"-surface showing a minimap in the top right corner
- the "main_map"-surface containing the map data at original size
- the "scaled_map"-surface, a scaled copy of the main_map remade every iteration to prevent 
data-loss on the original map-surface
"""

import pygame
from pygame.display import get_window_size as screen_size
from map_handler import map
import event_handler
import threading

    
def init():
    # convert the surfaces for adjusting their alpha values
    for surface in all: surface = surface.s.convert()
    clear()
    
def clear(): 
    # fill the surfaces in one color
    for surface in all: surface.s.fill((234,227,204))
    for surface in all:
        surface.s.set_alpha(120)
    main.s.set_alpha(150)
        

# the surface classes have a variable s and a pos.
# s represents their actual surface, pos is the position of the top - left corner of the surface.
       
# defining the main surface
class main:
    s = pygame.Surface(screen_size(),pygame.SRCALPHA)
    pos = (0,0)
    
    # function to update the scaled map if necessary and blit it to the main surface
    def update_map():
        if event_handler.scroll != 0: scaled_map.update_on_zoom()
        if event_handler.move != (0,0): scaled_map.update_on_move()
        scaled_map.reset_pos_if_out_of_bounds()
        main.s.blit(scaled_map.s, scaled_map.pos)

# this class is for the stats-surface
class stats:
    s = pygame.Surface((300,200),pygame.SRCALPHA)
    pos = (20,screen_size()[1]-220)

# this class is for the controll-surface
class controll:
    s = pygame.Surface((250,250),pygame.SRCALPHA)
    pos = (screen_size()[0]-270,screen_size()[1]-270)

# this class is for the minimap-surface
class minimap:
    s = pygame.Surface((200,200),pygame.SRCALPHA)
    background_surface = pygame.Surface((0,0))
    mask_surface = pygame.Surface((200,200))
    pos = (screen_size()[0]-230, 30)
    
    def init():
        minimap.background_surface = pygame.transform.smoothscale(original_map.s,(200,200))
        minimap.mask_surface.convert()
        minimap.mask_surface.set_alpha(100)
    def update():
        minimap.mask_surface.fill((150,150,140))
        w_mult = 200/scaled_map.s.get_width()
        h_mult = 200/scaled_map.s.get_height()
        rect_x = int(-scaled_map.pos[0]*w_mult)
        rect_y = int(-scaled_map.pos[1]*h_mult)
        rect_w = screen_size()[0]*w_mult
        rect_h = screen_size()[1]*h_mult
        pygame.draw.rect(minimap.mask_surface,(234,227,204), (rect_x,rect_y,rect_w,rect_h))
        pygame.draw.rect(minimap.mask_surface,(0,0,0), (rect_x,rect_y,rect_w,rect_h),2)
        
        minimap.s.blit(minimap.background_surface,(0,0))
        minimap.s.blit(minimap.mask_surface,(0,0))
        pygame.draw.rect(minimap.background_surface,(0,0,0), (0,0,200,200),2)
    

# this class is for the original map
class original_map:
    s = pygame.Surface((map.width*50, map.height*50))
    pos = (0,0)

# this class is for the scaled map
class scaled_map:
    
    # variables for the zoom function
    # the zoom variable sais the scaled width/height of one tile
    zoom = 5
    current_zoom_step = 0
    zoom_steps = (5,7,8,9,10,12,14,16,19,22,26,31,37,44,52,62,74,88,100)
    pos = (0,0)
    s = pygame.Surface((0,0))
    surf_cache = {}
    
    # cache loading function using threading
    # by using threads, the loading time of the Bad Mergentheim Map was reduced by 45% (7.5s -> 4.1s on the Heitec laptops)
    def load_cache(progress_surface: pygame.Surface):
        threads = []
        for i in scaled_map.zoom_steps:
            thread = threading.Thread(target=scaled_map.cache_thread_process, args=(original_map.s, i, progress_surface))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
    def cache_thread_process(image, i, progress_surface):
        size = map.width*i
        scaled_image = pygame.transform.smoothscale(image.copy(), (size,size))
        scaled_map.surf_cache[str(i)] = scaled_image
        # update the loading screen
        loading_surface.current_step += 1
        pygame.event.get()
        loading_surface.update(progress_surface, progressbar=True)
        pygame.display.flip()
        
    # function to adjust the size of the surface and blitting the tiles for the first time 
    # to prevent a empty surface on start
    def init():
        size = main.s.get_width()
        scaled_map.s = scaled_map.surf_cache["5"]
    
    # handling zoom events
    def update_on_zoom():
        mz = max(0, scaled_map.current_zoom_step+event_handler.scroll)
        scaled_map.current_zoom_step = min(len(scaled_map.zoom_steps)-1, mz)
        scaled_map.zoom = scaled_map.zoom_steps[scaled_map.current_zoom_step]
        
        oldMapW = scaled_map.s.get_width()
        scaled_map.s = scaled_map.surf_cache[str(scaled_map.zoom)]
        newMapW = scaled_map.s.get_width()
        
        mpos = pygame.mouse.get_pos()
        posx = mpos[0] - (mpos[0]-scaled_map.pos[0])/oldMapW * newMapW
        posy = mpos[1] - (mpos[1]-scaled_map.pos[1])/oldMapW * newMapW
        scaled_map.pos = (posx,posy)
    
    # handling moving events
    def update_on_move():
        x,y = scaled_map.pos
        rx,ry = event_handler.move
        scaled_map.pos = (x+rx, y+ry)
    
    # preventing the map to be pulled of the screen
    def reset_pos_if_out_of_bounds():
        minMapSize = scaled_map.surf_cache["5"].get_width()
        maxOffsetMovingToRight = (main.s.get_width()-minMapSize)//2
        maxOffsetMovingToLeft = screen_size()[0] - maxOffsetMovingToRight - scaled_map.s.get_width()
        maxOffsetMovingDown = max(0,(main.s.get_height()-minMapSize)//2)
        maxOffsetMovingUp = min(screen_size()[1]-minMapSize,screen_size()[1] - maxOffsetMovingDown - scaled_map.s.get_height())
        x = min(maxOffsetMovingToRight, max(scaled_map.pos[0], maxOffsetMovingToLeft))
        y = min(maxOffsetMovingDown, max(scaled_map.pos[1], maxOffsetMovingUp))
        scaled_map.pos = (x, y)
      
# this class is for the loading screen      
class loading_surface:
    s = pygame.Surface(screen_size())
    message = ""
    current_step = 0
    steps = len(scaled_map.zoom_steps)
    progress = 0
    big_font = pygame.font.SysFont("Century Gothic", 60, True)
    small_font = pygame.font.SysFont("Century Gothic", 25, True)
    loading_text = big_font.render("LOADING...", True, (0,0,0))
    
    # function to update and show the loading screen
    def update(target: pygame.Surface, message=None, progressbar=False):
        loading_surface.s.fill((234,227,204))
        loading_surface.s.blit(loading_surface.loading_text, ((screen_size()[0] - loading_surface.loading_text.get_width())//2, 200))
        if progressbar:
            loading_surface.progress = int(loading_surface.current_step/loading_surface.steps*100)
            start_x = (screen_size()[0] - 40*loading_surface.steps)//2
            for i in range(len(scaled_map.zoom_steps)):
                if i < loading_surface.current_step: pygame.draw.rect(loading_surface.s, (0,255,0), (start_x+40*i, 300, 40, 15))
                else: pygame.draw.rect(loading_surface.s, (255,0,0), (start_x+40*i, 300, 40, 15))
        if message is None: message = "Precalculating surfaces... [ "+str(loading_surface.current_step)+"/"+str(loading_surface.steps)+" - ( "+str(loading_surface.progress)+"% ) ]"
        text = loading_surface.small_font.render(message, True, (0,0,0))
        loading_surface.s.blit(text, ((screen_size()[0] - text.get_width())//2, 350))
        target.blit(loading_surface.s, (0,0))

# store some surfaces in a tupel to loop through them later
all = (main,stats,controll,minimap)