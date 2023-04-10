import pygame
import random
import math

class Map:
    
    def __init__(self, seed, width, height, min_height = None, max_height = None) -> None:
        self.seed = seed
        self.ground_colour = (0, 0, 0)
        self.points = {}
        self.width = width
        self.height = height
        self.min_height = min_height
        self.max_height = max_height
        self.generate_map()
        
    def order_points(self):
        self.points = dict(sorted(self.points.items()))
        
    def draw_points(self, screen):
        pass
    
    def get_height(self, x):
        pass
    
    def get_draw_height(self, x):
        pass
    
    def get_point_at(self, pos):
        pass
        
    def generate_map(self):
        pass
            
if __name__ == "__main__":
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    map = Map(0, screen.get_width(), screen.get_height())
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                break
            
        screen.fill((255, 255, 255))
        map.draw_points(screen)
        pygame.display.flip()
        
    pygame.quit()