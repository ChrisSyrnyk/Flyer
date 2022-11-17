import random
class obstacle:
    #init variables
    def __init__(self, width = 0):
        self._width = width
    def __init__(self, height = 0):
        self._height = height
    def __init__(self, x = 0):
        self._x = x
    def __init__(self, y = 0):
        self._y = y
    #getters
    def get_width(self):
        return self._width
    def get_height(self):
        return self._height    
    def get_x(self):
        return self._x
    def get_y(self):
        return self._y
    #setters
    def set_width(self, x):
        self._width = x
    def set_height(self, x):
        self._height = x
    def set_x(self, x):
        self._x = x
    def set_y(self, x):
        self._y = x

    #methods for defining obstacle movement
    def move_down(self):    #could add speed which is an attribute of the class obstacle
        self._y += 0.25

    #methods for determining object start dimensions and position
    def new_parameters(self):
        #reset y to 0
        self._y = 0
        #randomonly determine width with max being half screen 250x
        self._width = random.randint(50, 250)
        #determine left, right or middle
        l_or_right = random.randint(0,2)
        #if left set x to 0
        if (l_or_right == 0):
            self._x = 0
        elif (l_or_right == 1):
            self._x = (250 - (self._width/2))   
        else:
            self._x = (500 - self._width)
        #else set x to 500 - width 
    #check end and reset position (screen dimension are 500x 800y) not going to change these.
    def reset_y(self):
        if (self._y == 800):
            self.new_parameters()
            
#global variable 
obstacles = []  #list containing obstacles. can use methods from obstacle class to access and set attributes of object

#function for generating num*obstacles
def createObstacles(num):
    i = 0
    while(i<num):
        newObstacle = obstacle() #create new obstacle
        newObstacle.new_parameters() #set obstacle parameters
        newObstacle.set_height(20) #set obstacle height
        #logic for determing object start height
        newObstacle.set_y(-i * (800/num)) #i determine obstacle number. 800 is height of window. 800/num = even spacing. multiplied by its position.
        obstacles.append(newObstacle) #add to list of obstacles
        i+=1 #increment counter

#function for moving obstacles down the screen
def moveObstacles():
    for obstacle in obstacles: #for each obstacle in obstacles 
        obstacle.move_down()    #move down

#function for moving obstacles back to top of screen once bottom reached
def resetObstacles():
    for obstacle in obstacles:  #for each obstacle in obstacles
        obstacle.reset_y()  #reset y position to 0
        
#set start position of obstacles
def obstacles_set_start():
    i = 0
    for obstacle in obstacles:
        obstacle.set_y(-i * (800/len(obstacles)))
        i+=1

#game counter
obstacles_cleared = -1 #account for obstacle hit on collision being added to obstacles cleared
def increment_obstacles_cleared():
    global obstacles_cleared
    obstacles_cleared += 1
def reset_obstacles_cleared():
    global obstacles_cleared
    obstacles_cleared = 0

#create obstacles
createObstacles(6) #input value for number of objects. more objects increases difficulty

