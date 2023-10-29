import pygame
import sys
import os
import random
#import required modules
# yup making changes on my branch whooooop
vec = pygame.math.Vector2
#allows for shorthand to be used to save time

GREEN = (143, 254, 9)
BROWN = (210,105,30)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (166,16,0)
#defines the colour constants

WIDTH = 1200
HEIGHT = 500
FONT_NAME = 'arial'
#defines other constants

PLAYER_FR = -0.11
GRAVITY = 0.4
PLAYER_ACC = 0.6
#defines player mechanics constants


class Player(pygame.sprite.Sprite):

    def __init__(self,game):

        super().__init__()

        self._layer = 0
        self.image_left = pygame.image.load(os.path.join("assets/player","player_left.png"))
        self.image_right = pygame.image.load(os.path.join("assets/player","player_right.png"))
        self.image_down = pygame.image.load(os.path.join("assets/player","player_down.png"))    
        #loads images of player facing in either directions and the player when downed
        
        self.image_left.set_colorkey(WHITE)
        self.image_right.set_colorkey(WHITE)
        self.image_down.set_colorkey(WHITE)
        #sets a colourkey so pixels turn clear if player image
        #colour matches the background
        

        self.image = self.image_right      
        self.rect = self.image.get_rect()
        self.rect2 = self.image.get_rect()
        #obtains correct starting image and creates rect
        
        self.game = game
        self.acc = vec(0,0)
        self.vel = vec(0,0)
        self.pos = vec(WIDTH/2,HEIGHT/2)
        self.gun_pos = vec(0,0)
        #uses the vector function to setup 2D vectors for
        #acceleration, velocity and inital position

        self.player_direction_right = True
        #flag for determining player direction

    def update(self):
                    
        self.acc = vec(0,GRAVITY)
        #ensures the player is accelerated downwards every frame

        if self.game.keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
            self.image = self.image_left
            self.player_direction_right = False
            #accelerates player left and orientates sprite

        if self.game.keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC
            self.image = self.image_right
            self.player_direction_right = True
            #accelerates player right and orientates sprite

        if self.game.keys[pygame.K_UP]:
            self.jump()
            #calls jump function if space pressed

        self.rect = self.image.get_rect()
        self.acc.x += self.vel.x * PLAYER_FR
        #ensures a maximum speed exists by ensuring friction is
        #proportional to speed
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        #equations of motion that translate acceleration and velocity to
        #positional movement
        
        self.rect.midbottom = self.pos
        #sets the players postion to midbottom

        self.zombie_hit = pygame.sprite.spritecollide(self,self.game.enemy_group, False)
        #checks for collision between the player and any zombie in the zombie sprite group
        
        if self.zombie_hit:
            self.game.screen.blit(self.image_down,[self.pos.x-20,self.pos.y-60])
            #draws the image of the player downed onto the screen
            self.game.game_over()
            #calls the game over function

    def jump(self):

        hit = pygame.sprite.spritecollide(self,self.game.platform, False)
        #checks for collision between player and platform
        
        if hit:
            self.jumping = True
            self.vel.y = -10
            #gives an inital y velocity to propel upwards


class Weapon(pygame.sprite.Sprite):

    def __init__(self,game,filename,damage,fire_rate,adjustment):

        super().__init__()
        #all the methods from the parent class are inherited

        self.game = game
        #allows for methods and attributes within the main class to be referenced

        self.damage = damage
        self.fire_rate = fire_rate
        self.adjustment = adjustment
        #assigns the damage and fire rate variables to attributes
        
        self.image_right = pygame.image.load(os.path.join("assets/weapons",filename))
        #loads in the desired image
        
        self.image_right = pygame.transform.scale2x(self.image_right)
        #doubles image in size
       
        self.image_left = pygame.transform.flip(self.image_right,True,False)
        #creates a flipped version of image for use when gun is facing other way
        
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.rect.center = [self.game.player.pos.x,self.game.player.pos.y]
        #creates the rect and positions it at the players coordinates
        
        self.timer = 0
        #sets the timer

    def update(self):

        if self.game.player.player_direction_right:
            self.image = self.image_right
            #if the player is facing right then so will the gun

        if not self.game.player.player_direction_right:
            self.image = self.image_left
            #if the player is facing left then so will the gun

        self.rect.center = [self.game.player.pos.x,self.game.player.pos.y-20]
        #sets the guns position to the players pos every frame

        if self.game.keys[pygame.K_SPACE]:

            self.shoot()
            #if the up arrow pressed then shoot function called

    def shoot(self):

        self.time_elapsed = pygame.time.get_ticks()
        #gets total time elapsed
        
        if self.time_elapsed - self.timer > self.fire_rate*1000:
            
            self.timer = self.time_elapsed
            #if time is above certain time set based on gun fire rate, then shoot
            
            self.bullet1 = Bullet(self.game,self.game.player.player_direction_right,self.damage)
            #creates a bullet object
            self.game.bullet_group.add(self.bullet1)
            #adds bullet instance to sprite group


class Bullet(pygame.sprite.Sprite):

    def __init__(self,game,direction,damage):

        super().__init__()
        #all the methods from the parent class are inherited
        
        self.game = game
        #allows for methods and attributes within the main class to be referenced
        self.direction = direction
        self.damage = damage
        #assigns the damage and direction for each bullet based on the weapon direction
        #and damage

        self.bullet_r = self.game.bullet_right
        self.bullet_l = self.game.bullet_left
        #obtains the images that have been loaded in the main class

        self.vel = vec(0,0)
        self.pos = vec(self.game.player.pos.x,self.game.player.pos.y-20 - \
                       self.game.current_weapon.adjustment)
        #creates vel and pos vectors and assigned the position to
        #the position of thegun and adjusts it to match the gun barrel height
      
        if direction: #if gun is facing right

            self.image = self.bullet_r
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.vel = vec(20,0)
            #sets the images position and creates velocity in the direction of gun

        if not direction: #if gun facing left

            self.image = self.bullet_l
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.vel = vec(-20,0)
            #sets the images position and creates velocity in the
            #direction of gun

    def update(self):

        self.pos += self.vel
        self.rect.center = self.pos
        #adds the velocity to pos, allowing image to change position

        if 0 > self.pos.x or self.pos.x > WIDTH:

            self.kill()
            #if the bullet goes off the screen it is removed


class Enemy(pygame.sprite.Sprite):

    def __init__(self,game,health,speed):

        super().__init__()
        #all the methods from the parent class are inherited

        self.game = game
        #allows for methods and attributes within the main class to be referenced
        
        self.health = health
        self.speed = speed
        #assigns the health and acc speed for enemy

        self.image_right = self.game.zombie_right
        self.image_left = self.game.zombie_left
        #fetches images loaded in main class

        self.image = self.image_right
        self.rect = self.image.get_rect()
        #gets rect so position can be changed
        
        self.acc = vec(0,0)
        self.vel = vec(0,0)
        #creates vectors for movement
        
        spawn_choice = bool(random.getrandbits(1))
        #obtains random number 1/0 and turns that into boolean

        if spawn_choice:
            self.pos = vec(WIDTH,HEIGHT/2)
            #if true then enemy spawns on right side

        if not spawn_choice:
            self.pos = vec(0,HEIGHT/2)
            #if false then enemy spawns on left side

        self.rect.midbottom = self.pos
        #sets the position to mid bottom

    def update(self):
        self.acc = vec(0,GRAVITY)
        #ensures the enemy is accelerated downwards every frame
        pos1 = round(self.game.player.pos.x,-1)
        pos2 = round(self.pos.x,-1)
        #gets rounded versions of player pos x and enemy pos x
        
        if pos1 < pos2:
            self.acc.x = -self.speed
            self.image = self.image_left
            #accelerates enemy left and orientates sprite if player is to the left
            #of the enemy
        elif pos1 > pos2:
            self.acc.x = self.speed
            self.image = self.image_right
            #accelerates enemy right and orientates sprite if player is
            #to the rightof the enemy
        else:
            self.acc.x = 0
            #if player is in same x pos as enemy, it stops moving

        self.acc.x += self.vel.x * PLAYER_FR
        #ensures a maximum speed exists by ensuring friction is proportional to speed
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        #equations of motion that translate acceleration and velocity to
        #positional movement
        
        self.rect.midbottom = self.pos
        self.hit = pygame.sprite.spritecollide(self,self.game.platform,False)
        #checks for platform collision
        if self.hit:
            self.vel.y = 0
            self.acc.y = 0
            self.pos.y = self.hit[0].rect.top
            self.plat_hit = True
            #if colliding with platform, adjust position so it
            #does not fall through

        self.bullet_hit = pygame.sprite.spritecollide(self,self.game.bullet_group,False)
        if self.bullet_hit:
            self.health -= self.bullet_hit[0].damage
            self.bullet_hit[0].kill()
            
        if self.health <= 0:
            self.kill()
            self.game.zombie_remain -= 1
            #if the enemy health reached zero, then it is
            #removed from all sprites


class Setting(pygame.sprite.Sprite):

    def __init__(self,filename):
        #colour, width, height and xy coordinates are taken in as parameters
        
        super().__init__()
        #all the methods from the parent class are inherited
        
        self.image = pygame.image.load(os.path.join("assets/setting",filename))
        #the image to be used is loaded

        self.rect = self.image.get_rect()
        #the rect of the surface is obtained

        if filename == "room.png":
            self.image = pygame.transform.scale(self.image,(WIDTH,HEIGHT))
            #scales the image to fit within the size of game window
            self.rect.x = 0
            self.rect.y = 0
            #the coordinated of the rect is placed at the desired location

        if filename == "corridor.png":
            self.image = pygame.transform.scale(self.image,(WIDTH,HEIGHT))
            #scales the image to fit within the size of game window
            self.rect.x = 0
            self.rect.y = 60
            #the coordinated of the rect is placed at the desired location

        if filename == "city.png":
            self.rect.x = 0
            self.rect.y = -20
            #the coordinated of the rect is placed at the desired location


class Platform(pygame.sprite.Sprite):

    def __init__(self,colour,width,height,x,y):
        #colour, width, height and xy coordinates are taken in as parameters
        
        super().__init__()
        #all the methods from the parent class are inherited
        
        self.image = pygame.Surface([width, height])
        self.image.fill(colour)
        #a rectangular surface is created, given dimensions and a colour

        self.rect = self.image.get_rect()
        #the rect of the surface is obtained

        self.rect.x = x
        self.rect.y = y
        #the coordinated of the rect is placed at the desired location


class Object(pygame.sprite.Sprite):

    def __init__(self,game,filename,x,y):
        #filename and xy coordinates are taken in as parameters
        
        super().__init__()
        #all the methods from the parent class are inherited

        self.game = game
        #allows for methods and attributes within the
        #main class to be referenced

        self.image = pygame.image.load(os.path.join("assets/weapons",filename))
        #the image is loaded

        self.rect = self.image.get_rect()
        #the rect of the iamge is obtained

        self.rect.midbottom = [x,y]
        #the coordinated of the image is placed at the desired location

        self.interact = False
        #flag to check for interaction

    def update(self):

        self.hit = pygame.sprite.spritecollide(self,self.game.player_group,False)
        #checks for collision betweeen object weapon itself and the player

        if self.hit and self.game.keys[pygame.K_e]:
            #if there is a collision and "e" key is pressed

            self.interact = True
            #sets flag to true

        else:
            self.interact = False
            #else the flag is false


class Game(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()
        #initialises parent class - pygame sprite class

        pygame.init()
        pygame.mixer.init()
        #initialises pygame modules

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Survival Horror Arcade Game")
        #defines the pygame display size and caption

        self.font_name = pygame.font.match_font(FONT_NAME)
        self.clock = pygame.time.Clock()
        self.running = True
        #sets the font, defines the clock as an attribute and sets the running flag
        
    def new(self):

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player_group = pygame.sprite.Group()
        self.platform = pygame.sprite.Group()
        self.weapon_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.object_group = pygame.sprite.Group()
        self.setting_group = pygame.sprite.Group()
        #creates sprite groups, so required sprites can be updated and
        #drawn on when needed
        
        self.player = Player(self)
        #instantiates a player object

        self.player_group.add(self.player)
        #adds the player to the sprite group

        self.player_scene = 0
        #creates an attribute which will be used to track which scene the player is in

        self.plat1 = Platform(BLACK,WIDTH,20,0,HEIGHT-20)
        self.plat2 = Platform(BLACK,WIDTH,20,0,HEIGHT-20)
        self.plat3 = Platform(BLACK,WIDTH,20,0,HEIGHT-20)
        #defines the basic platforms

        self.weapon_ppsh = Weapon(self,"ppsh.png",15,0.05,5)
        self.weapon_bar = Weapon(self,"bar.png",50,0.3,5)
        self.weapon_mg42 = Weapon(self,"mg42.png",40,0.1,15)
        self.weapon_kar98k = Weapon(self,"kar98k.png",20,0.75,5)
        self.weapon_mp40 = Weapon(self,"mp40.png",10,0.05,15)
        self.weapon_stg44 = Weapon(self,"stg44.png",20,0.07,15)
        self.weapon_bren = Weapon(self,"bren.png",50,0.5,0)
        #creates objects for all usable weapons and gives them different abilities

        self.object_ppsh = Object(self,"ppsh.png",600,HEIGHT-20)
        self.object_bar = Object(self,"bar.png",250,HEIGHT-20)
        self.object_mg42 = Object(self,"mg42.png",1000,HEIGHT-20)
        self.object_kar98k = Object(self,"kar98k.png",300,HEIGHT-20)
        self.object_mp40 = Object(self,"mp40.png",650,HEIGHT-20)
        self.object_stg44 = Object(self,"stg44.png",900,HEIGHT-20)
        self.object_bren = Object(self,"bren.png",1100,HEIGHT-20)
        #creates objects for all the wepaon obhjects that can be picked up and
        #specifies their location to be placed
               
        self.current_weapon = self.weapon_kar98k
        #instantiates weapon object
        
        self.weapon_group.add(self.weapon_kar98k)
        #add weapon to weapon group

        self.bullet_right = pygame.image.load(os.path.join("assets/weapons","bullet.png"))
        self.bullet_right = pygame.transform.scale(self.bullet_right,(75,35))
        self.bullet_left = pygame.transform.flip(self.bullet_right,True,False)
        #loads bullet images

        self.zombie_right = pygame.image.load(os.path.join("assets/enemy","zombie.png"))
        self.zombie_right = pygame.transform.scale2x(self.zombie_right)
        self.zombie_left = pygame.transform.flip(self.zombie_right,True,False)
        #loads the zombie images

        self.round = 1
        self.zombie_no = 0
        self.zombie_remain = 0
        self.spawn_timer = 0
        self.respawn_timer = 0
        #attributes for use with spawning zombies

        self.respawn = False
        #flag for respawning zombies when scene is changed

        self.room_image = Setting("room.png")
        self.corridor_image = Setting("corridor.png")
        self.city_image = Setting("city.png")
        #creates instances of Setting class using filenames for the backgrounds

        self.ambience = pygame.mixer.Sound(os.path.join("assets/sounds","ambience.wav"))
        #creates a sound by loading the sound file
        self.ambience_channel = pygame.mixer.Channel(1)
        #creates a channel to play the sound on

    def run(self):
        self.playing = True
        #sets a flag to indicate game in running
        while self.playing:
            self.clock.tick(60)
            self.keys = pygame.key.get_pressed()
            self.events()
            self.update()           
            self.draw()
            #defines an entire clock cycle at 60Hz and indicates all the events 
            #that should take place such as updating and drawing sprites
            
    def update(self):

        self.platform.empty()
        self.object_group.empty()
        self.setting_group.empty()
        #empties all platforms from the group so correct one can be added
        #every frame
        
        if self.player_scene == 0:
            self.platform.add(self.plat1)
            #adds the platform
            self.setting_group.add(self.room_image)
            #adds the correct background image to be used for the scene
            self.object_group.add(self.object_mp40)
            self.object_group.add(self.object_bren)
            #adds the correct guns to be able to be picked up in the scene
            
        if self.player_scene == 1:           
            self.platform.add(self.plat2)
            #adds the platform
            self.setting_group.add(self.corridor_image)
            #adds the correct background image to be used for the scene
            self.object_group.add(self.object_stg44)
            self.object_group.add(self.object_ppsh)
            #adds the correct guns to be able to be picked up in the scene
         

        if self.player_scene == 2:            
            self.platform.add(self.plat3)
            #adds the platform
            self.setting_group.add(self.city_image)
            #adds the correct background image to be used for the scene
            self.object_group.add(self.object_mg42)
            self.object_group.add(self.object_bar)
            #adds the correct guns to be able to be picked up in the scene
 
        #dependent upon which scene, the correct platform and object weapons will be added

        if self.object_mp40.interact:
            #mp40 interacted with
            self.weapon_group.empty()
            #weapon group emptied
            self.weapon_group.add(self.weapon_mp40)
            self.current_weapon = self.weapon_mp40
            #mp40 added and set as current weapon

        if self.object_bren.interact:
            #bren interacted with
            self.weapon_group.empty()
            #weapon group emptied
            self.weapon_group.add(self.weapon_bren)
            self.current_weapon = self.weapon_bren
            #bren added and set as current weapon


        if self.object_stg44.interact:
            #stg interacted with
            self.weapon_group.empty()
            #weapon group emptied
            self.weapon_group.add(self.weapon_stg44)
            self.current_weapon = self.weapon_stg44
            #stg added and set as current weapon

        if self.object_ppsh.interact:
            #ppsh interacted with
            self.weapon_group.empty()
            #weapon group emptied
            self.weapon_group.add(self.weapon_ppsh)
            self.current_weapon = self.weapon_ppsh
            #ppsh added and set as current weapon

        if self.object_mg42.interact:
            #mg42 interacted with
            self.weapon_group.empty()
            #weapon group emptied
            self.weapon_group.add(self.weapon_mg42)
            self.current_weapon = self.weapon_mg42
            #mg42 added and set as current weapon

        if self.object_bar.interact:
            #bar interacted with
            self.weapon_group.empty()
            #weapon group emptied
            self.weapon_group.add(self.weapon_bar)
            self.current_weapon = self.weapon_bar
            #bar added and set as current weapon
            

        self.hit = pygame.sprite.spritecollide(self.player,self.platform,False)
        #checks for collision between player and platforms

        if self.hit:
            self.player.vel.y = 0
            self.player.acc.y = 0
            self.player.pos.y = self.hit[0].rect.top
            self.plat_hit = True
            #if collision detected then y vel and acc stopped and
            #position set to on top the platform
        
        self.player_group.update()
        self.weapon_group.update()
        self.bullet_group.update()
        self.enemy_group.update()
        self.object_group.update()
        #all sprites updated

    def events(self):

        pos = round(self.player.pos.x,-1)
        #rounds the x coordinate of the player so it can be compared easier
        
        self.event_list = pygame.event.get()
        #obtains list of all events occuring in the frame
            
        for event in self.event_list: #fetches all events in the frame
            
            if event.type == pygame.QUIT: #if user quits              
                self.playing = False
                self.running = False
                #if player close application then loops broken and program ends

        if pos == WIDTH and self.player_scene != 2:

            self.respawn = True
            self.enemy_group.empty()
            self.respawn_left = self.zombie_remain
            #flag for respawning zombies when scene is changed
       
            self.player_scene += 1
            self.player.pos.x = 5
            #allows the scene to change if player reaches right end of screen

        if pos == 0 and self.player_scene != 0:

            self.respawn = True
            self.enemy_group.empty()
            self.respawn_left = self.zombie_remain
            #flag for respawning zombies when scene is changed
            
            self.player_scene += -1
            self.player.pos.x = WIDTH-5
            #allows the scene to change if player reaches left end of screen

        if self.round == 1: #during first round
            if self.zombie_no < 5: #until 5 zombies have spawned
                self.time_elapsed = pygame.time.get_ticks() #gets total time passed
                if self.time_elapsed - self.spawn_timer > 500:
                    self.enemy_group.add(Enemy(self,100,0.2))
                    #creates zombie object and adds to group
                    self.spawn_timer = self.time_elapsed
                    self.zombie_no += 1
                    self.zombie_remain += 1
                    #if more than 0.5 secs have passed since last zombie spawn then
                    #add zombies until 5 have spawned

            if self.zombie_remain == 0:
                self.zombie_no = 0
                self.round += 1
                #if there are no zombies left then enter next round

        if self.round == 2:#during second round
            if self.zombie_no < 7:
                self.time_elapsed = pygame.time.get_ticks()#gets total time passed
                if self.time_elapsed - self.spawn_timer > 500: 
                    self.enemy_group.add(Enemy(self,110,0.2))
                    #creates zombie object and adds to group
                    self.spawn_timer = self.time_elapsed
                    self.zombie_no += 1
                    self.zombie_remain += 1
                    #if more than 0.5 secs have passed since last zombie spawn then
                    #add zombies until 5 have spawned

            if self.zombie_remain == 0:
                self.zombie_no = 0
                self.round += 1
                #if there are no zombies left then enter next round

        if self.round > 2:#during higher rounds
            if self.zombie_no < 10:
                self.time_elapsed = pygame.time.get_ticks()#gets total time passed
                if self.time_elapsed - self.spawn_timer > 100:
                    self.enemy_group.add(Enemy(self,150,0.3))
                    #creates zombie object and adds to group
                    #zombies have more health and speed
                    self.spawn_timer = self.time_elapsed
                    self.zombie_no += 1
                    self.zombie_remain += 1
                    #if more than 0.45 secs have passed since last zombie spawn then
                    #add zombies until 5 have spawned

            if self.zombie_remain == 0:
                self.zombie_no = 0
                self.round += 1
                #if there are no zombies left then enter next round

        if self.respawn:
            #if bool is true
            
            if self.respawn_left > 0:
                self.time_elapsed = pygame.time.get_ticks()#gets total time passed
                if self.time_elapsed - self.respawn_timer > 500:
                    #if more than 0.5 secs has passed
                    if self.round < 3:
                        #if round is less than 3
                        self.enemy_group.add(Enemy(self,100,0.2))
                        #adds zombie of correct health and speed according to round
                    else:
                        self.enemy_group.add(Enemy(self,150,0.3))
                        #adds zombie of correct health and speed according to round
                                         
                    #creates zombie object and adds to group
                    self.respawn_timer = self.time_elapsed
                    self.respawn_left -= 1
                    #subtract 1 from attribute      
    
        if not self.ambience_channel.get_busy():
            #checks if the sound is currently playing
            self.ambience_channel.play(self.ambience)
            #play the sound on the channel

    def draw(self):
   
        self.screen.fill(BLACK) #create background       
        self.platform.draw(self.screen)
        self.setting_group.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.object_group.draw(self.screen)
        self.player_group.draw(self.screen)
        self.enemy_group.draw(self.screen)        
        self.bullet_group.draw(self.screen)
        self.weapon_group.draw(self.screen)    
        #draws on all sprites that exist within these sprite groups

        self.draw_text(str(self.round),50, RED, 25, 20)
        #draws text in the top left corner to signify the round
        
        #draws on all sprites, background and text

        pygame.display.flip()
        #flips sprites onto screen


    def menu(self):

        self.screen.fill(BLACK)
        #black background
        self.draw_text("Press any key to play", 25, WHITE, WIDTH/2, HEIGHT*(3/4))
        self.draw_text("Survival Horror Arcade", 91, RED, WIDTH/2, HEIGHT*(1/4))
        self.draw_text("Survival Horror Arcade", 90, WHITE, WIDTH/2, HEIGHT*(1/4)-4)
        #draws the text, which includes a red shadow affect
        pygame.display.flip()
        #updates display
        waiting = True
        while waiting:
            #loop here to keep user in menu until they proceed or exit
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    #if they close pygame then progam closes
                    self.running = False
                    #sets the main running flag to false to end game
                if event.type == pygame.KEYUP:
                    waiting = False
                    #if they press a button, menu loop breaks and proceeds to game

    def game_over(self):
        self.draw_text("GAME OVER", 100, RED, WIDTH/2, 250)
        self.gameover_sound = pygame.mixer.Sound(os.path.join("assets/sounds","gameover1.wav"))
        self.gameover_sound.play()
        pygame.display.flip()
        waiting = True
        while waiting:
            #loop here to keep user in menu until they proceed or exit
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameover_sound.fadeout(3000)
                    waiting = False
                    #if they close pygame then progam closes
                    self.running = False
                    #sets the main running flag to false to end game
                if event.type == pygame.KEYUP:
                    self.gameover_sound.fadeout(3000)
                    waiting = False
                    self.new()
                    #if they press a button, game over loop breaks and proceeds to game
        

    def draw_text(self,text,size,colour,x,y):

        font = pygame.font.Font(self.font_name, size)
        #selects the font and the size
        text_surface = font.render(text, True, colour)
        #uses the font and the size to render the desired text
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        #gets the position of the text and places it in desired position
        self.screen.blit(text_surface, text_rect)
        #outputs it to screen
    
g = Game()
#creates instance of main class
g.menu()
#calls menu function
while g.running:
    #while the game is running

    g.new()
    #creates new game and loads all assets
    g.run()
    #calls the method for the main game loop

pygame.mixer.quit()
#exits the mixer module
pygame.quit()
#exits pygame
quit()
#closes program

