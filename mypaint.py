import pygame
pygame.init() # initializes all the pygame sub-modules

clock = pygame.time.Clock()
WIDTH = 640
HEIGHT = 480

LMBpressed = False
THICKNESS = 5
colorRED = (255, 0, 0)
colorBLUE = (0, 0, 255)
colorWHITE = (255, 255, 255)
colorBLACK = (0, 0, 0)

currX = 0
currY = 0
palette=0
prevX = 0
prevY = 0
FPS = 60 
current_shape = "rect" # constants
colors=[colorRED, colorBLUE, colorWHITE] #list of colors
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #creating the screen
base_layer = pygame.Surface((WIDTH, HEIGHT)) #creating off-screen drawing surface

def calculate_rect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2)) # calculating the xy pos and width and height of it

def calculate_square(x1,y1,x2,y2):
    side=max(abs(x2-x1),abs(y2-y1)) #take one length for width and height
    return pygame.Rect(min(x1,x2), min(y1,y2), side,side) # calculating the xy pos and side of it
def calculate_rhombus(cx,cy,d1,d2):
    p1=(cx, cy-d2/2) #top
    p2=(cx+d1/2, cy) #right
    p3=(cx, cy+d2/2) #bottom
    p4=(cx-d1/2, cy) #left
    return [p1,p2,p3,p4] #calculating points of rhombus
def calculate_eqtri(x1, y1, x2, y2):
    base_length=abs(x2-x1)
    height=(3**0.5 /2) *base_length
    p1=(min(x1,x2), max(y1,y2))
    p2=(max(x1,x2), max(y1,y2))
    p3=((x1+x2)/2, max(y1,y2)-height)
    return [p1,p2,p3]
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print("LMB pressed!")
            LMBpressed = True
            prevX = event.pos[0]
            prevY = event.pos[1] # When pressed store the previous position
        
        if event.type == pygame.MOUSEMOTION:
            print("Position of the mouse:", event.pos)
            if LMBpressed:
                currX = event.pos[0]
                currY = event.pos[1] # Store the current position
                screen.blit(base_layer, (0, 0))  # restore base layer to avoid overwriting
                if current_shape=="rect":
                    pygame.draw.rect(screen, colors[palette], calculate_rect(prevX, prevY, currX, currY), THICKNESS)  # draw rectangle with current color
                elif current_shape=='circle':
                    pygame.draw.circle(screen, colors[palette],  (prevX, prevY), int(((currX - prevX)**2 + (currY - prevY)**2)**0.5), THICKNESS) #draw circle with current color
                elif current_shape == "eraser":
                    pygame.draw.rect(screen, colorBLACK, calculate_rect(prevX, prevY, currX, currY))  # Erase part of the drawing
                pygame.display.flip()  # update
            
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            print("LMB released!")
            LMBpressed = False  # switch the flag
            currX = event.pos[0]
            currY = event.pos[1]
            if current_shape=="rect":
                pygame.draw.rect(screen, colors[palette], calculate_rect(prevX, prevY, currX, currY), THICKNESS)  # draw rectangle with current color
            elif current_shape=="square":
                pygame.draw.rect(screen, colors[palette], calculate_square(prevX, prevY, currX, currY), THICKNESS) # draw square with current color
            elif current_shape=='circle':
                pygame.draw.circle(screen, colors[palette],  (prevX, prevY), int(((currX - prevX)**2 + (currY - prevY)**2)**0.5), THICKNESS) #draw circle with current color
            elif current_shape=='right_triangle':
                p1=(prevX, prevY) #right angle point
                p2=(prevX,currY) #vertical point
                p3=(currX,prevY) #horizontal point
                pygame.draw.polygon(screen, colors[palette], [p1, p2, p3], THICKNESS) #draw right triangle with current color
            elif current_shape=="rhombus":
                d1=abs(currX-prevX)
                d2=abs(currY-prevY) #finding diagonals
                cx=(prevX+currX)/2
                cy=(prevY+currY)/2 #finding centers
                pygame.draw.polygon(screen, colors[palette], calculate_rhombus(cx, cy, d1, d2), THICKNESS) #draw rhombus with current color
            elif current_shape=="equilateral_triangle":
                pygame.draw.polygon(screen, colors[palette], calculate_eqtri(prevX, prevY, currX, currY), THICKNESS) #draw equilateral triangle with current color
            elif current_shape == "eraser":
                pygame.draw.rect(screen, colorBLACK, calculate_rect(prevX, prevY, currX, currY))  # Erase part of the drawing
            pygame.display.flip()  # update
            base_layer.blit(screen, (0, 0))  # save the current state of the screen
        
        if event.type == pygame.KEYDOWN:  # When a key is pressed
            if event.key == pygame.K_EQUALS:  # When + key is pressed
                print("increased thickness")
                THICKNESS += 1  # increase the thickness
            if event.key == pygame.K_MINUS:  # When - key is pressed
                print("reduced thickness")
                THICKNESS-=1  # decreases, but prevent thickness from becoming negative or zero
            if event.key == pygame.K_r:  # Switch to rectangle mode
                print("Switched to rectangle mode")
                current_shape = "rect"
            if event.key == pygame.K_s:  # Switch to square mode
                print("Switched to square mode")
                current_shape = "square"
            if event.key==pygame.K_t:  # Switch to right triangle mode
                print("Switched to right triangle mode")
                current_shape = "right_triangle"
            if event.key == pygame.K_c:  # Switch to circle mode
                print("Switched to circle mode")
                current_shape = "circle"
            if event.key == pygame.K_h:  # Switch to rhombus mode
                print("Switched to rhombus mode")
                current_shape = "rhombus"
            if event.key == pygame.K_q:  # Switch to equilateral triangle mode
                print("Switched to equilateral triangle mode")
                current_shape = "equilateral_triangle"
            if event.key == pygame.K_e:  # Switch to eraser mode
                print("Switched to eraser mode")
                current_shape = "eraser"
            if event.key == pygame.K_p:  # Switch to color mode
                print("Switched color")
                palette+=1
                palette%=3 #moving through list of colors

clock.tick(FPS)  #speed of game

pygame.quit()