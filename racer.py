import pygame
import time
import random
pygame.init()  # initializes all the pygame sub-modules

WIDTH = 400
HEIGHT = 600
RED = (255, 0, 0) 
PLAYER_SPEED = 5
ENEMY_SPEED = 10
delta_speed=5
need_coin=5 # constants

crash_sound = pygame.mixer.Sound("resources/crash.wav")
coin_sound = pygame.mixer.Sound("resources/coin.mp3")
background_music = pygame.mixer.music.load('resources/background.wav') # sounds and music

background = pygame.image.load("resources/AnimatedStreet.png") #back pic

font1 = pygame.font.SysFont("Verdana", 60)
game_over = font1.render("Game Over", True, "black") #text



pygame.mixer.music.play(-1)  # loop background music

screen = pygame.display.set_mode((WIDTH, HEIGHT)) # creating the screen

clock = pygame.time.Clock()
FPS = 60 #setting fps

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("resources/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(self.rect.w, WIDTH - self.rect.w), 0) #class for enemy

    def move(self):
        self.rect.move_ip(0, ENEMY_SPEED)
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(self.rect.w, WIDTH - self.rect.w), 0) #func for movement of enemy

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("resources/Player.png")
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - self.rect.w // 2
        self.rect.y = HEIGHT - self.rect.h #class for player

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-PLAYER_SPEED, 0)
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(PLAYER_SPEED, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH #func for movement of player



class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        coin_images=[
            "resources/coin1.png",
            "resources/coin2.png",
            "resources/coin3.png"
        ] #coins with different images
        
        self.image = pygame.image.load(coin_images[random.randrange(0,3)]) #randomly choosing coins
        self.rect = self.image.get_rect() 
        self.rect.x = random.randint(0, WIDTH - self.rect.w)
        self.rect.y = random.randint(-100, -40) #class for coin

    def respawn(self):
        self.rect.x = random.randint(0, WIDTH - self.rect.w)
        self.rect.y = random.randint(-100, -40) #changing location
    def move(self):
        self.rect.move_ip(0, 5)  # Falling speed of coins
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.w)
            self.rect.y = random.randint(-100, -40) #respawning 
            
def create_coins(num_coins):
    coins=pygame.sprite.Group()
    for i in range(num_coins):
        coin=Coin()
        coins.add(coin)
    return coins #as we now need more than one coin we create as many objects as in num_coins, and add them to the sprite group

enemy = Enemy() # creating objects
player=Player()
coins=create_coins(3) #create 3 coins with randomly diff weigths
enemies = pygame.sprite.Group()
enemies.add(enemy)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)
all_sprites.add(coins) # creating sprite groups
collected_coins = 0
running=True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  #game loop

    
    for entity in all_sprites:
        entity.move() #moving objects

    # checking for collision between player and enemy
    if pygame.sprite.spritecollideany(player, enemies):
        crash_sound.play()
        screen.fill(RED)
        center_rect = game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over, center_rect)
        pygame.display.flip()
        time.sleep(2)  # Wait for a moment before quitting
        running = False  # End the game
    
    for coin in coins:
        if pygame.sprite.spritecollideany(player,  coins): #as player earns coin
            coin_sound.play() #back sound
            collected_coins+=1 #coin calculation
            coin.respawn() #appereance of a new coin

            if collected_coins%need_coin==0:
                ENEMY_SPEED+=delta_speed #each time when we earn certain amount of coin our speed increases
    
    screen.blit(background, (0, 0))  # back pic
    font2 = pygame.font.SysFont("Verdana", 30)
    coin_text = font2.render(f"Coins: {collected_coins}", True, "black")
    screen.blit(coin_text, (WIDTH - 150, 20))#text coins 

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)  # show sprites on screen

  
    pygame.display.flip() #update

    clock.tick(FPS) #set the fps

pygame.quit()  # Exit