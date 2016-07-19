from microbit import *

class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def off(self):
        display.set_pixel(self.x, self.y, 0)
        
    def on(self):
        display.set_pixel(self.x, self.y, 9)
        
    def move(self, delta_x, delta_y):
        self.off()
        self.x = self.x + delta_x
        self.y = self.y + delta_y
        self.on()

class Pod(object):
    
    def __init__(self, left_point, right_point):
        self.left_point = left_point
        self.right_point = right_point
        
    def on(self):
        self.left_point.on()
        self.right_point.on()
        
    def move_left(self):
        if self.left_point.x > 0:
            self.left_point.move(-1, 0)
            self.right_point.move(-1, 0)
            
    def move_right(self):
        if self.right_point.x < 4:
            self.right_point.move(1, 0)
            self.left_point.move(1, 0)
            
            
class Movement(object):
    
    def __init__(self, point, delta_x, delta_y):
        self.point = point
        self.delta_x = delta_x
        self.delta_y = delta_y

    def process_edge(self):
        if self.point.y == 0:
            self.delta_y = self.delta_y * -1
        if self.point.x == 0 or self.point.x == 4:
            self.delta_x = self.delta_x * -1
        if self.point.y == 4:
            raise GameOverError

    def process_pod(self, pod):
        next_x = self.point.x
        if self.point.y == 3 and self.delta_y > 0: 
            if next_x == pod.left_point.x or next_x == pod.right_point.x:
                self.delta_y = self.delta_y * -1

    def move(self): 
        self.process_edge()
        self.point.move(self.delta_x, self.delta_y)
 

class GameOverError(RuntimeError):
    pass
    
pod = Pod(Point(2, 4), Point(3, 4))
pod.on()

ball = Movement(Point(0, 0), -1, -1)

while True:
    if button_a.is_pressed():
        pod.move_left()
        
    if button_b.is_pressed():
        pod.move_right()
    
    ball.process_pod(pod)
    try:
        ball.move()
    except GameOverError:
        ball.point.off()
        pod.on()
        sleep(2000)
        ball = Movement(Point(0, 0), -1, -1)
        
    sleep(200)

# Write your code here :-)