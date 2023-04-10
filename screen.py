import pygame
import random
import math

class Map:
    
    def __init__(self, seed, width, height, min_height = None, max_height = None, detail = 15) -> None:
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
        for point, value in self.points.items():
            if value:
                neighbours = self.get_neighbours(point)
                if len(neighbours) < 8:
                    for neighbour in neighbours:
                        if len(self.get_neighbours(neighbour)) < 7:
                            if (neighbour, point) not in drawn_lines:
                                pygame.draw.line(screen, self.ground_colour, point, neighbour)
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
        y_values = []
        if x % self.detail == 0:
            for point in self.points.keys():
                if point[0] == x and self.points[point]:
                    up_point = (point[0], point[1] - self.detail)
                    if (up_point in self.points and not self.points[up_point]) or up_point not in self.points:
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

    def generate_map(self):
        random.seed(self.seed)
        seed_heights = {}
        if not self.min_height: self.min_height = math.floor(self.height * 0.9)
        if not self.max_height: self.max_height = math.ceil(self.height * 0.3)
        last_height = random.randint(self.max_height, self.min_height)
        for x in range(-self.detail, self.width + self.detail, self.detail):
            for y in range(self.max_height - self.detail, self.height + self.detail, self.detail):
                self.points[(x, y)] = False
            
            last_height = random.randint(last_height - self.detail*2, last_height + self.detail*2)
            if last_height < self.max_height: last_height = self.max_height
            if last_height > self.min_height: last_height = self.min_height
            seed_heights[x] = last_height
                
        for point in self.points.keys():
            if point[1] > seed_heights[point[0]]:
                self.points[point] = True
            
if __name__ == "__main__":
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    map = Map(random.randint(-100000, 100000), screen.get_width(), screen.get_height())
    running = True
    right_clicked = False
    left_clicked = False
    middle_clicked = False
    while running:
        
        screen.fill((255, 255, 255))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                break
            
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
                    
        if right_clicked:
            mousex, mousey = pygame.mouse.get_pos()
            points = map.get_nearest_points((mousex, mousey), map.detail * 2)
            for point in points:
                map.points[point] = False
                
        if middle_clicked:
            mousex, mousey = pygame.mouse.get_pos()
            points = map.get_nearest_points((mousex, mousey), map.detail * 2)
            for point in points:
                map.points[point] = True
                
        if left_clicked:
            mousex, mousey = pygame.mouse.get_pos()
            y_values = map.get_heights_at(mousex)    
            for y in y_values:
                pygame.draw.circle(screen, (255, 0, 0), (mousex, y), 2)
            
        map.draw_points(screen)
        pygame.display.flip()
        
    pygame.quit()