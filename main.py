from functions import *
import math
import random
import pygame
import pygame_gui

pygame.init()


#--------------------------------- Configurations
# --- setting screen size
SCREEN = WIDTH, HEIGHT = 1300, 512
# --- setting FPS of the game
FPS = 60
# ---- Getting values of displayed windows
info = pygame.display.Info()
width = info.current_w
height = info.current_h
# ---- Scalling window size
if width >= height:
    win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else:
    win = pygame.display.set_mode(
        SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)
# ---- Declaring Colors that we are going to use
BLACK = (18, 18, 18)
WHITE = (217, 217, 217)
RED = (252, 0, 0)
GREEN = (29, 161, 16)
BLUE = (78, 193, 246)
ORANGE = (252, 76, 2)
YELLOW = (254, 221, 0)
PURPLE = (155, 38, 182)
AQUA = (0, 249, 182)
COLORS = [RED, GREEN, BLUE, ORANGE, YELLOW, PURPLE]
# ---- Adjusting Font size and Type
font = pygame.font.SysFont('verdana', 12)
# ----- Declaring Background Image to fit screen
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
# ------ Declaring goal image
goal_image = pygame.image.load("goal.png")
goal_image = pygame.transform.scale(goal_image, (100, 150))
# ---------------------------- Intial Conditons
# ----- Goal Position
goal_pos = (900, 200)
# ----- Orgin position where ball is shot
origin = (60, 340)
# ----- intial velocity
u = 20
# ----- Gravity acceleration
g = 9.8
# ----- initial distance from goal
distance = 25
#------ intial bottom clicking condition
clicked = False
#------ the we gonna assing it later velocity and angel
currentp = None
#------ intial angle
theta = -30

clock = pygame.time.Clock()

# @desc: function used to draw the goal picture which is declared in config. at specific position
def draw_net():
    win.blit(goal_image, goal_pos)

# @desc: function used to add an input box for controlling value of intial velocity
def create_input_box(manager):
    input_rect = pygame.Rect(WIDTH - 150, 280, 100, 20)
    input_text = pygame_gui.elements.UITextEntryLine(
        relative_rect=input_rect, manager=manager)
    input_text.set_allowed_characters('numbers')
    input_text.set_text(str(u))
    return input_text

# @desc: function used to add an input box for controlling value of distance of ball from the goal
def create_origin_input_box(manager):
    input_rect = pygame.Rect(WIDTH - 150, 300, 100, 20)
    input_text = pygame_gui.elements.UITextEntryLine(
        relative_rect=input_rect, manager=manager)
    input_text.set_allowed_characters('numbers')
    input_text.set_text(str(distance))
    return input_text


# @desc: function used to calculate the elevation distance at goal line
def calculate_ball_elevation_at_goal(distance, velocity, angle):
    # Convert the angle from degrees to radians
    angle_rad = angle

    # Calculate the time taken to reach the goal plane
    time_to_goal = distance / (velocity * math.cos(angle_rad))

    # Calculate the vertical displacement at the goal plane
    vertical_displacement = (
        velocity * math.sin(angle_rad) * time_to_goal) - (0.5 * 9.8 * time_to_goal**2)
    
    return vertical_displacement

#used to add elemets in the project
manager = pygame_gui.UIManager((WIDTH, HEIGHT))
#adding inputbox related to distance calculation
origin_input_box = create_origin_input_box(manager)
#adding inputbox related to velocity calculation
input_box = create_input_box(manager)

# @desc: class includes the projectile methods and attributes for the (simulation only) not actual calculations
class Projectile(pygame.sprite.Sprite):
    def __init__(self, u, theta):
        super(Projectile, self).__init__()
        #----- Class Attributes
        #--velocity multipled by a factor inorder to simulate its momevent in pixels correctly
        self.u = u * 6
        #--Angle of the projectile
        self.theta = toRadian(abs(theta))
        #--Orgin(ball start position)
        self.x, self.y = origin
        #-- Ball color
        self.color = random.choice(COLORS)
        #-- scale
        self.ch = 0
        self.dx = 2
        # The trajectory represents the horizontal distance traveled by the projectile before hitting the ground,
        # assuming that the projectile is launched from the ground level and lands at the same level.
        self.f = self.getTrajectory()
        #getting total range corresponding to start postion
        self.range = self.x + abs(self.getRange())
        # storing different values of x and y values during the path (inorder to be able to draw them later on)
        self.path = []
    #----- Class methods
    def timeOfFlight(self):
        return round((2 * self.u * math.sin(self.theta)) / g, 2)
    
    def getRange(self):
        range_ = ((self.u ** 2) * 2 * math.sin(self.theta)
                  * math.cos(self.theta)) / g
        return round(range_, 2)

    def getMaxHeight(self):
        h = ((self.u ** 2) * (math.sin(self.theta)) ** 2) / (2 * g)
        return round(h, 2)

    def getTrajectory(self):
        return round(g / (2 * (self.u ** 2) * (math.cos(self.theta) ** 2)), 4)

    def getProjectilePos(self, x):
        return x * math.tan(self.theta) - self.f * x ** 2
    
    def update(self):
        # we check if ball entered the goal yet or not to stop it from moving
        if self.x >= (goal_pos[0]+5) and self.y >= (goal_pos[1]):
            self.dx = 0
        # we clear the ball if goes out of the screen
        if self.x >= self.range:
            self.dx = 0
        # we add the change in x distance to the old value of x
        self.x += self.dx
        # get the new relative postion of the x
        self.ch = self.getProjectilePos(self.x - origin[0])
        # we appened both value x and y of the path
        self.path.append((self.x, self.y-abs(self.ch)))
        self.path = self.path[-50:]
        #we draw the ball at each point on the path
        pygame.draw.circle(win, RED, self.path[-1], 10)
        pygame.draw.circle(win, WHITE, self.path[-1], 6, 2)
        pygame.draw.circle(win, WHITE, self.path[-1], 4, 2)
        pygame.draw.circle(win, WHITE, self.path[-1], 2, 2)
        # drawing the small balls behind the big ball which represents the curvature of path
        for pos in self.path[:-1:4]:
            pygame.draw.circle(win, RED, pos, 1)

#creating an instance
projectile_group = pygame.sprite.Group()

end = getPosOnCircumeference(theta, origin)
arct = toRadian(theta)
arcrect = pygame.Rect(origin[0]-30, origin[1]-30, 60, 60)


running = True
while running:
    # time relative to FPS
    time_delta = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                running = False

            if event.key == pygame.K_r:
                projectile_group.empty()
                currentp = None

        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True

        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
            # Get the position of the mouse on the screen
            pos = event.pos
            # specify are for lanching
            launch_area_rect = pygame.Rect(
                origin[0], origin[1] - 250, 250, 250)
            # Check if the click position is within the launch area
            if launch_area_rect.collidepoint(pos):
                # calculate angle of the mouse from orgin point
                theta = getAngle(pos, origin)
                # Check the angle of the mouse
                if -90 < theta <= 0:
                    if currentp:
                        # Remove the previous ball
                        projectile_group.remove(currentp)
                    # creating an object from proectile class and assigning values u and theta
                    projectile = Projectile(u, theta)
                    projectile_group.add(projectile)
                    currentp = projectile

        if event.type == pygame.MOUSEMOTION:
            #if we clocked the botton of mouse
            if clicked:
                #we get postion of the mouse
                pos = event.pos
                #based on pos we get the angle where mouse is at inorder to decide the value of the angle
                theta = getAngle(pos, origin)
                #check if the angle is in the correct range (-90 and 0) relative to screen 
                if -90 < theta <= 0:
                    end = getPosOnCircumeference(theta, origin)
                    arct = toRadian(theta)

        manager.process_events(event)

    manager.update(time_delta)

    if -90 < theta <= 0:
        end = getPosOnCircumeference(theta, origin)
        arct = toRadian(theta)
    #we draw everything in sequence here (order is important)
    win.blit(background_image, (0, 0))
    draw_net()
    pygame.draw.line(win, BLACK, origin, (origin[0] + 900, origin[1]), 2)
    pygame.draw.line(win, BLACK, origin, (origin[0], origin[1] - 200), 2)
    pygame.draw.line(win, BLACK, origin, end, 2)
    pygame.draw.circle(win, BLACK, origin, 3)
    arcrect = pygame.Rect(origin[0]-30, origin[1]-30, 60, 60)
    pygame.draw.arc(win, RED, arcrect, 0, -arct, 2)
    projectile_group.update()
    #pinting the output values
    title = font.render("Projectile Motion", True, WHITE)
    degreetext = font.render(f"{int(abs(theta))}°", True, YELLOW)
    win.blit(title, (80, 30))
    win.blit(degreetext, (origin[0]+38, origin[1]-20))
    #if mouse is pressed and object currenttp (which is the the current object(ball))exists 
    #pritn all values
    if currentp:
        veltext = font.render(f"Velocity : {currentp.u/6}m/s", True, BLACK)
        timetext = font.render(f"Time : {timeOfFlight(currentp.u/6,currentp.theta)}s", True, BLACK)
        rangetext = font.render(f"Range : {getRange(currentp.u/6,currentp.theta)}m", True, BLACK)
        heighttext = font.render(f"Max Height : {getMaxHeight(currentp.u/6,currentp.theta)}m", True, BLACK)
        ball_at_goal = calculate_ball_elevation_at_goal(distance, currentp.u/6, currentp.theta)
        if(ball_at_goal < 0):
            ball_elevation_at_goal = font.render(f"Ball height at goal :Not reached ", True, BLACK)
        else:
            ball_elevation_at_goal = font.render(f"Ball height at goal :{round(ball_at_goal, 2)}m", True, BLACK)
    #specifying location of text on screen before showing them
        win.blit(veltext, (WIDTH-200, 400))
        win.blit(timetext, (WIDTH-200, 420))
        win.blit(rangetext, (WIDTH-200, 440))
        win.blit(heighttext, (WIDTH-200, 460))
        win.blit(ball_elevation_at_goal, (WIDTH-200, 480))
    #input boxes viewing
    #--- inputs for velocity box
    inputVelocitytext = font.render(f"Input Velocity :", True, BLACK)
    inputVelocityparamtext = font.render("m/sec", True, BLACK)
    win.blit(inputVelocitytext, (WIDTH-240, 280))
    win.blit(inputVelocityparamtext, (1250, 280))
    #--- inputs for distance box
    origin_input_text = font.render(f"Input Distance :", True, BLACK)
    win.blit(origin_input_text, (WIDTH-240, 300))
    origin_input_text = font.render("m", True, BLACK)
    win.blit(origin_input_text, (1250, 300))
    #if the box value changed means accept the incoming new value and recalculate values based on it
    if origin_input_box.text != '' and int(origin_input_box.text) != distance:
        new_distance = int(origin_input_box.get_text().strip())
        pygame.draw.arc(win, BLACK, arcrect, 0, -arct, 2)
        if new_distance != distance:
            distance = new_distance
            origin = (900-distance*33.6, origin[1])

    pygame.draw.rect(win, (0, 0, 0), (0, 0, WIDTH, HEIGHT), 5)

    # Draw the input box
    manager.draw_ui(win)

    # Check if the input box value has changed
    if input_box.text != '' and int(input_box.text) != u:
        new_u = int(input_box.get_text().strip())

        if new_u != u:
            u = new_u

            if currentp:
                currentp.u = u
                
    pygame.display.update()

pygame.quit()
