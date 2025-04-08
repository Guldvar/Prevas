import pygame
import random

class Rollercoaster:

    def __init__(self, points = 10):
        self.points = [1] * points

    def update(self):
        self.points.pop(0)
        curPoint = self.points[-1]
        if curPoint == 0:
            newPoint = random.randint(1, 3)
        else: 
            r = random.random()
            if r < 0.05:
                newPoint = 0
            elif r < 0.60:
                newPoint = curPoint
            elif r < 0.80:
                newPoint = curPoint - 1
            else:
                newPoint = curPoint + 1
        
        print(curPoint, newPoint)
        self.points.append(newPoint)
        return self.points

    #def draw(self, screen):
    #    pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


rc = Rollercoaster()
print(rc.points)
for _ in range(10):
    rc.update()
print(rc.points)