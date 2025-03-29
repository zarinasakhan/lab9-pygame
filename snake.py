import pygame
import random
import time
pygame.init() # initializes all the pygame sub-modules

WIDTH = 600
HEIGHT = 600
CELL = 30  # Constants

colorRED = (255, 0, 0)
colorYELLOW = (255, 255, 0)
colorGREEN = (0, 255, 0)
colorGRAY = (169, 169, 169)
colorWHITE = (255, 255, 255) # Colors

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # creating the screen

def draw_grid():
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)  # dividing the screen into cells with borders

def draw_grid_chess():
    colors = [colorWHITE, colorGRAY] 
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))  # drawing 2 colored cells 

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x}, {self.y}" #creatin class point for drawing objects

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0  #direction of snake, initially it moves to the right, creation of class snake

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y #shifting each segment to the position of previous one
        self.body[0].x += self.dx #changing direction
        self.body[0].y += self.dy

    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))  # drawing the red head
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))  # drawing yellow body

    def check_collision(self, food):
        head_x = self.body[0].x*CELL #converting into pixel coordinates
        head_y = self.body[0].y*CELL
        head_rect=pygame.Rect(head_x, head_y, CELL, CELL) 
        food_rect=pygame.Rect(food.rect.x, food.rect.y, food.size, food.size) #creating rectangles for both

        if head_rect.colliderect(food_rect): #if two rectangles overlaps(if snake eats food)
            self.body.append(Point(self.body[-1].x, self.body[-1].y))  # Snake body grows as it gets food (new point will be added to the end)
            return True
        return False

    def check_wall_collision(self):
        head = self.body[0]
        if head.x < 0 or head.x >= WIDTH // CELL or head.y < 0 or head.y >= HEIGHT // CELL:
            return True
        return False #Checking for border (wall) collision and whether the snake is leaving the playing area

class Food(pygame.sprite.Sprite):
    def __init__(self, snake,time_limit=5):
        super().__init__()
        self.snake = snake
        self.size=random.randrange(CELL // 2, CELL) #foods' sizes will change randomly in range of 15 to 30px
        self.pos = self.generate_food_pos()  # initialize food position
        self.image = pygame.Surface((self.size, self.size))  # create surface for the food
        self.image.fill(colorGREEN)  # fill the surface with green color
        self.rect = self.image.get_rect()  #get the position
        self.rect.x = self.pos.x * CELL + (CELL - self.size) // 2 #to food to be placed in center, not in top-left corner
        self.rect.y = self.pos.y * CELL + (CELL - self.size) // 2
        self.time_created = time.time()  # store the time the food was created
        self.time_limit = time_limit # set the expiration time (5 by default)

    def generate_food_pos(self):
        while True:
            x = random.randint(0, (WIDTH - self.size) // CELL)
            y = random.randint(0, (HEIGHT - self.size) // CELL)
            if not any(segment.x == x and segment.y == y for segment in self.snake.body): # checks if food is not placed on the snake's body
                return Point(x, y) #new posiiton randomly

    def update(self):
        if time.time() - self.time_created > self.time_limit:  # when the food has existed longer than the time limit:
            self.kill()  # remove  food from the sprite group
            food_group.add(Food(self.snake)) # add a new food 
            
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y)) #draw food

def create_foods(num_foods, snake):
    foods_group=pygame.sprite.Group()
    for i in range(num_foods):
        food=Food(snake)
        foods_group.add(food)
    return foods_group #as we now need more than one food we create as many foods as in num_foods and add them into sprite group

FPS = 5
score = 0
level = 0
clock = pygame.time.Clock() #variables to work with

snake = Snake() #create snake object
food_group = create_foods(3, snake) #creating 3 objects of food


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # game loop
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.dx = 1
                snake.dy = 0
            elif event.key == pygame.K_LEFT:
                snake.dx = -1
                snake.dy = 0
            elif event.key == pygame.K_DOWN:
                snake.dx = 0
                snake.dy = 1
            elif event.key == pygame.K_UP:
                snake.dx = 0
                snake.dy = -1  # snake's movement with keyboard keys

    snake.move() #make snake move by the func
    for food in food_group:
        food.update()  # check if food has expired, if yes delete

    for food in food_group:
        if snake.check_collision(food):
            score += 1
            food.kill() #remove eaten food
            food_group.add(Food(snake))  # regenerate new food

    if snake.check_wall_collision():
        print("Game over: Snake hit the wall")
        running = False  #Checking for border (wall) collision and whether the snake is leaving the playing area

    if score >= 4:  # increase level every 4 foods eaten
        level += 1
        score = 0
        FPS += 1  # increase speed when level increases

    
    draw_grid_chess()
    snake.draw()
    for food in food_group:
        food.draw(screen) #draw all objects 
   
  
    font = pygame.font.SysFont("Verdana", 30)
    level_text = font.render(f"Level: {level}", True, "black")
    score_text = font.render(f"Score: {score}", True, "black")
    screen.blit(level_text, (WIDTH - 150, 20))
    screen.blit(score_text, (WIDTH - 150, 60))   # display score and level

    pygame.display.flip()
    clock.tick(FPS)  # the speed of the game

pygame.quit()  #exit