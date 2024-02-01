"""
This file manages the detection of user inputs.
"""
import pygame

# values change if input is detected
scroll = 0
move = (0,0)

# this function is done once every iteration
def main():
    # reset the values indicating whether there was a input
    global scroll, move
    scroll = 0
    move = (0,0)
    
    # check if pygame detected mouse or keyboard events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: quit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: quit()
        elif event.type == pygame.MOUSEWHEEL: scroll = event.y
    mouseRel = pygame.mouse.get_rel()
    if pygame.mouse.get_pressed(3)[0]: move = mouseRel