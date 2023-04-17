import pygame
import random
import math

pygame.init()
pygame.font.init()

class Map:
    
    def __init__(self, seed, width, height, min_height = None, max_height = None, detail = 10) -> None:
        self.seed = seed
        self.ground_colour = (0, 0, 0)
        self.points = {}
        self.width = width
        self.height = height
        self.min_height = min_height
        self.max_height = max_height
        self.detail = detail
        self.generate_map()
        
    def draw_points(self, screen):
        drawn_lines = []
        size_change = screen.get_width() / self.width
        for point, value in self.points.items():
            if value:
                neighbours = self.get_neighbours(point)
                if len(neighbours) < 8:
                    for neighbour in neighbours:
                        if len(self.get_neighbours(neighbour)) < 7:
                            if (neighbour, point) not in drawn_lines:
                                point1 = point[0] * size_change, point[1] * size_change
                                point2 = neighbour[0] * size_change, neighbour[1] * size_change
                                pygame.draw.line(screen, self.ground_colour, point1, point2)
                                drawn_lines.append((point, neighbour))
                
    def get_neighbours(self, point):
        neighbours = [(point[0], point[1] - self.detail),
                      (point[0], point[1] + self.detail),
                      (point[0] - self.detail, point[1]),
                      (point[0] + self.detail, point[1]),
                      (point[0] + self.detail, point[1] + self.detail),
                      (point[0] - self.detail, point[1] - self.detail),
                      (point[0] - self.detail, point[1] + self.detail),
                      (point[0] + self.detail, point[1] - self.detail)
                    ]
        
        to_return = []
        for neighbour in neighbours:
            if neighbour in self.points and self.points[neighbour]:
                to_return.append(neighbour)
                
        return to_return

    def get_nearest_points(self, point_clicked, radius):
        points = []
        for point in self.points:
            dx = point[0] - point_clicked[0]
            dy = point[1] - point_clicked[1]
            if math.hypot(dy, dx) <= radius:
                points.append(point)
                
        return points
    
    def get_heights_at(self, x):
        x = round(x)
        y_values = []
        if x % self.detail == 0:
            for point in self.points.keys():
                if point[0] == x and self.points[point]:
                    up_point = (point[0], point[1] - self.detail)
                    if up_point in self.points and not self.points[up_point]:
                        y_values.append(point[1])
                        
                    elif up_point not in self.points:
                        y_values.append(point[1])
                      
        else:
            after_cal_ys = []
            previous_x = math.floor(x / self.detail) * self.detail
            for point1 in self.points.keys():
                if point1[0] == previous_x and self.points[point1]:
                    for point2 in self.points.keys():
                        if point2[0] == previous_x + self.detail and self.points[point2]:
                            dy = point2[1] - point1[1]
                            
                            if dy == 0:
                                
                                up1 = (point1[0], point1[1] - self.detail)
                                up2 = (point2[0], point2[1] - self.detail)
                                if not (up1[1] < self.max_height or up2[1] < self.max_height):
                                    if self.points[up1] and self.points[up2]:
                                        continue
                                    
                                    after_cal_ys.append(point1[1])
                                    
                                else:
                                    after_cal_ys.append(self.max_height)
                            
                            elif abs(dy) == self.detail:
                                
                                up1 = (point1[0], point1[1] - self.detail)
                                up2 = (point2[0], point2[1] - self.detail)
                                if up1[1] < self.max_height: up1 = (up1[0], self.max_height)
                                if up2[1] < self.max_height: up2 = (up2[0], self.max_height)
                                
                                if self.points[up1] and self.points[up2]:
                                    continue
                                
                                percentage_x = (x / self.detail) % 1
                                y = point1[1] + (dy * percentage_x)
                                after_cal_ys.append(y)
            
            if len(after_cal_ys) > 0:
                after_cal_ys.sort()
                y_values.append(after_cal_ys[0])
                for _ in range(len(after_cal_ys)//3):
                    y_values.append(after_cal_ys[-3 * _])
                                                         
        return y_values
    
    def get_size_change(self, screen_width):
        return screen_width / self.width

    def generate_map(self):
        random.seed(self.seed)
        seed_heights = {}
        if not self.min_height: self.min_height = math.floor(self.height * 0.9)
        if not self.max_height: self.max_height = math.ceil(self.height * 0.1)
        last_height = random.randint(self.max_height, self.height // 2)
        for x in range(-self.detail, self.width + self.detail, self.detail):
            for y in range(self.max_height, self.height + self.detail, self.detail):
                self.points[(x, y)] = False
            
            last_height = random.randint(last_height - self.detail*2, last_height + self.detail*2)
            if last_height < self.max_height: last_height = self.max_height + self.detail
            if last_height > self.min_height: last_height = self.min_height - self.detail
            seed_heights[x] = last_height
                
        for point in self.points.keys():
            if point[1] >= seed_heights[point[0]]:
                self.points[point] = True
                
class Screen:
    
    def __init__(self, map = None) -> None:
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.map = None
        self.running = False
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.font = pygame.font.SysFont(None, 24)
        self.text_colour = (255, 0, 0)
        if self.map:
            self.size_change = self.map.get_size_change(self.screen.get_width())
        
    def set_map(self, map):
        self.map = map
        self.size_change = self.map.get_size_change(self.screen.get_width())
        
    def display_text(self):
        fps_text = self.font.render(f"FPS: {round(self.clock.get_fps())}", True, self.text_colour)
        seed_text = self.font.render(f"Seed: {self.map.seed if self.map else None}", True, self.text_colour)
        
        self.screen.blit(fps_text, (2, 2))
        self.screen.blit(seed_text, (2, 26))
        
    def mainloop(self):
        self.running = True
        right_clicked = False
        left_clicked = False
        middle_clicked = False
        
        if self.map:
            self.size_change = self.map.get_size_change(self.screen.get_width())
            
        while self.running:
            
            self.screen.fill((255, 255, 255))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.set_map(Map(random.randint(-1000, 1000), 1000, 1000, detail=5))
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        left_clicked = True
                        
                    if event.button == 2:
                        middle_clicked = True
                        
                    if event.button == 3:
                        right_clicked = True
                        
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        left_clicked = False
                        
                    if event.button == 2:
                        middle_clicked = False
                        
                    if event.button == 3:
                        right_clicked = False
                        
            if right_clicked and self.map:
                mousex, mousey = pygame.mouse.get_pos()
                points = self.map.get_nearest_points((mousex / self.size_change, mousey / self.size_change), map.detail * 2)
                for point in points:
                    self.map.points[point] = False
                    
            if middle_clicked and self.map:
                mousex, mousey = pygame.mouse.get_pos()
                points = self.map.get_nearest_points((mousex / self.size_change, mousey / self.size_change), map.detail * 2)
                for point in points:
                    self.map.points[point] = True
                    
            if left_clicked and self.map:
                mousex, mousey = pygame.mouse.get_pos()
                y_values = self.map.get_heights_at(mousex / self.size_change)    
                for y in y_values:
                    pygame.draw.circle(self.screen, (255, 0, 0), (mousex, y * self.size_change), 2)
            
            if self.map:
                self.map.draw_points(self.screen)
                
            self.display_text()
            pygame.display.flip()
            
            self.clock.tick(self.FPS)
            
        pygame.quit()
            
if __name__ == "__main__":
    screen = Screen()
    map = Map(69, 1000, 1000)
    #screen.set_map(map)
    screen.mainloop()