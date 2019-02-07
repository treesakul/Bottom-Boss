import pygame, sys
event = None
mouse_pos = None

#initializing colors
red = (180,42,42)
light_red = (250,92,92)
grey = (205,197,191)
dimGrey = (139,134,130)
white = (255,255,255)
black = (0,0,0)
yellow = (255,255,0)
purple = (96,35,122)

#player's class
class Player(pygame.sprite.Sprite):
    def __init__(self,color = (0,0,0), width = 64, height = 64):
        super(Player, self).__init__()
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.hspeed = 0
        self.vspeed = 0
        self.facing = 'right'
        self.blood = 3
        self.alive = 1
        self.win = 0
        self.fire = Sound("click.wav")
        self.finish = Sound("fire.wav")
        
#set position of the player
    def set_pos(self,x,y):
        self.rect.x = x
        self.rect.y = y

#set how fast the player can walk
    def change_speed(self,h,v):
        self.hspeed += h
        self.vspeed += v
#player's properties
    def set_properties(self):
        self.rect = self.image.get_rect()
        self.origin_x = self.rect.centerx
        self.origin_y = self.rect.centery
        self.speed = 8
        
#set image of the player      
    def set_image(self, filename = None):
        if(filename != None):
            self.image = pygame.image.load(filename).convert_alpha()
            self.set_properties()
            
#check if the player ris dead by checking the blood if so the plyer is not alive
    def checkDeath(self):
        if(self.blood <0):
            self.alive = 0

#update the player reaction to the walls, monsters, bullets, finish line and bottom line
    def update(self, collidable = pygame.sprite.Group(),
               monstercollide = pygame.sprite.Group(),
               fire_list = pygame.sprite.Group(),
               end_block = pygame.sprite.Group(),
               finish_block = pygame.sprite.Group(),
               blood_block = pygame.sprite.Group(),event = None):
            
        self.gravity() #call the gravity function 
        
        self.rect.x += self.hspeed
        collision_list = pygame.sprite.spritecollide(self, collidable, False)
        monster_collision_list = pygame.sprite.spritecollide(self, monstercollide, True)
        finish_block_list = pygame.sprite.spritecollide(self, finish_block, False)

        #check in horizontal 
        for finish in finish_block_list: #check with the finish line
            if(self.hspeed >0):
                self.rect.right = finish.rect.left
                self.finish.update()
                self.win = 1
        for collided_object in collision_list: #check with the walls
            if(self.hspeed >0):
                self.rect.right = collided_object.rect.left
            elif(self.hspeed < 0):
                self.rect.left = collided_object.rect.right
                
        for collided_monster in monster_collision_list: #check with the monsters
            if(self.hspeed >=0):
                i = 1
                for blood in blood_block:       #player touches the monster
                    if(i == self.blood):            #blood decreased by one
                        blood_block.remove(blood)
                    i += 1
                self.blood -= 1
                self.rect.right = collided_monster.rect.left
                
            elif(self.hspeed <= 0):
                i = 1
                for blood in blood_block:
                    if(i == self.blood):
                        blood_block.remove(blood)
                    i += 1
                self.blood -= 1
                self.rect.left = collided_monster.rect.right
                
        #check in vertical 
        self.rect.y += self.vspeed
        collision_list = pygame.sprite.spritecollide(self, collidable, False)
        monster_collision_list = pygame.sprite.spritecollide(self, monstercollide, True)
        end_block_list = pygame.sprite.spritecollide(self, end_block, False)
                
        for collided_object in collision_list: #check with the wall
            if(self.vspeed >0):
                self.rect.bottom = collided_object.rect.top
                self.vspeed = 0
            elif(self.vspeed < 0):
                self.rect.top = collided_object.rect.bottom
                self.vspeed = 0
                
        for block in end_block_list:        #check with the bottom line
            if(self.vspeed > 0):
                self.rect.bottom == block.rect.top
                self.blood = -1

                
        for collided_monster in monster_collision_list: #check with thhe monster
            if(self.vspeed >=0):
                self.rect.bottom = collided_monster.rect.top
                i = 1
                for blood in blood_block:
                    if(i == self.blood):
                        blood_block.remove(blood)   #if player touches the monster
                    i += 1                       #blood decreased by 1
                self.blood -= 1
                self.vspeed = 0
            elif(self.vspeed < 0):
                self.rect.top = collided_monster.rect.bottom
                self.vspeed = 0      
        
        if not(event == None):                      #recieve the user's input
            if (event.type == pygame.KEYDOWN ):
                if(event.key == pygame.K_RIGHT):    #and check with the arrow keys
                    self.facing = 'right'
                    self.change_speed((self.speed),0)
                if(event.key == pygame.K_LEFT):
                    self.facing = 'left'
                    self.change_speed(-(self.speed),0)
                if(event.key == pygame.K_SPACE):
                    self.fire.update()
                    fire = Fire(self.rect.x+40, self.rect.y +20,self.facing, 10, 10)
                    fire_list.add(fire)
                    fire_list.update()

                if(event.key == pygame.K_UP):
                    if(self.vspeed == 0):
                        self.change_speed(0,-(self.speed*2))
                if(event.key == pygame.K_DOWN):
                    pass
            if (event.type == pygame.KEYUP ):
                if(event.key == pygame.K_RIGHT):
                    if self.hspeed != 0: self.hspeed = 0
                if(event.key == pygame.K_LEFT):
                    if self.hspeed != 0: self.hspeed = 0
                if(event.key == pygame.K_UP):
                    if self.vspeed != 0: self.vspeed = 0
                if(event.key == pygame.K_SPACE):
                    if self.vspeed != 0: self.vspeed = 0
                if(event.key == pygame.K_DOWN):
                    if self.vspeed != 0: self.vspeed = 0
                
        for fire_shoot in fire_list:    #check the fire if it touches the wall or the monster
            fire_shoot.update( monstercollide, collidable, fire_list)
            fire_shoot.run()
            if(fire_shoot.check):
                fire_list.remove(fire_shoot)
                
        self.checkDeath()   #check the status of the player
            
    def gravity(self,gravity = 0.5):        #force the player togo vertically down
        if self.vspeed == 0: self.vspeed = 1
        else: self.vspeed += gravity

#player's blood sprites
class Blood(pygame.sprite.Sprite): 
    def __init__(self,x,y,width, height, color = (0,0,0)):
        super(Blood, self).__init__()
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.image = pygame.image.load("blood.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
#block sprites used to creat blood, monster and walls 
class Block(pygame.sprite.Sprite):
    def __init__(self,x,y, width, height, filename = None):
        super(Block, self).__init__()
        self.image = pygame.Surface([width,height])
        self.image.fill((100,0,0))
        if filename != None:
            self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
                
#Monster objects 
class Monster(pygame.sprite.Sprite):
    
    def __init__(self,x,y, width, height, color = (0,0,0)):
        super(Monster, self).__init__()
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.image = pygame.image.load("monster.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.face = 'right'
    
    def run(self, speed):   #function force the monster to run automatically
        if(self.face == 'right'):
            self.rect.x += speed
        elif(self.face == 'left'):
            self.rect.x -= speed

    def update(self,wall_list = pygame.sprite.Group()): #change the direction if i hits the wall
        self.run(1)
        wall_collision = pygame.sprite.spritecollide(self, wall_list, False)
        
        for wall_object in wall_collision:
            if(self.face == 'right'):
                if self.rect.right >= wall_object.rect.left:
                    self.rect.right = wall_object.rect.left
                    self.face = 'left'
            elif(self.face == 'left'):
                if self.rect.left <= wall_object.rect.right:
                    self.rect.left = wall_object.rect.right
                    self.face = 'right'

#Fire or bullet objects        
class Fire(pygame.sprite.Sprite):
    
    def __init__(self,x,y,face, width, height, color = (0,0,0)):
        super(Fire, self).__init__()
        self.image = pygame.Surface([width,height])
        self.image.fill(purple)
        self.face = face
        self.image = pygame.image.load("bullet.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.fire_speed = 10
        self.check = 0
        
        
    def update(self,monster_list = pygame.sprite.Group(),
               wall_list = pygame.sprite.Group(),
               fire_list = pygame.sprite.Group()): #updte the bullet status
        

        monster_collision = pygame.sprite.spritecollide(self, monster_list, True)
        #the wmonster will disappear when the bullet touches
        wall_collision = pygame.sprite.spritecollide(self, wall_list, False)
        #the walls will not disappear when the bullet touches
        fire_collision = pygame.sprite.spritecollide(self, wall_list, False)
        #the bullets will not disappear when the bullet touches

        
            
        for monster_object in monster_collision:    #chek if the minster touches the bullets
            if(self.face == 'right'):
                if self.rect.right >= monster_object.rect.left:
                    self.check = 1
            elif(self.face == 'left'):
                if self.rect.left <= monster_object.rect.right:
                    self.check = 1
            
        for wall_object in wall_collision:      #check if the monster touches the wall
            if(self.face == 'right'):
                if self.rect.right >= wall_object.rect.left:
                    self.check = 1
            elif(self.face == 'left'):
                if self.rect.left <= wall_object.rect.right:
                    self.check = 1
    #force the bullets to move     
    def run(self):
        
        if self.face == 'right':
            self.rect.x += self.fire_speed
        else:
            self.rect.x -= self.fire_speed

#level object  
class Level(object):
    def __init__(self, player_object):
        
        self.object_list = pygame.sprite.Group()
        self.monster_list = pygame.sprite.Group()
        self.player_object = player_object
        self.end_block = pygame.sprite.Group()
        self.finish_block = pygame.sprite.Group()
        self.blood_block = pygame.sprite.Group()
        self.world_shift_x = 0
        self.world_shift_y = 0
        self.left_viewbox = 150
        self.right_viewbox = 350
        self.up_viewbox = 290
        self.down_viewbox = 200

    def update(self):   #update the position of objects in the level
        self.object_list.update()
        self.monster_list.update()
        self.end_block.update()
        self.finish_block.update()
        self.blood_block.update()

    def shift_world(self, shift_x, shift_y):    #move the objects equally
        self.world_shift_x += shift_x
        self.world_shift_y += shift_y
        for each_object in self.object_list:
            each_object.rect.x += shift_x
            each_object.rect.y += shift_y
        for each_monster in self.monster_list:
            each_monster.rect.x += shift_x
            each_monster.rect.y += shift_y
        for end in self.end_block:
            end.rect.x += shift_x
            end.rect.y += shift_y
        for finish in self.finish_block:
            finish.rect.x += shift_x
            finish.rect.y += shift_y
        
    def run_viewbox( self ):    #move the objects depending on the player's position
        
        if(self.player_object.rect.x <= self.left_viewbox):
            view_difference = self.left_viewbox - self.player_object.rect.x
            self.player_object.rect.x = self.left_viewbox
            self.shift_world(view_difference, 0)

        if(self.player_object.rect.x >= self.right_viewbox):
            view_difference = self.right_viewbox - self.player_object.rect.x
            self.player_object.rect.x = self.right_viewbox
            self.shift_world(view_difference, 0)
            
        if(self.player_object.rect.y <= self.up_viewbox):
            view_difference = self.up_viewbox - self.player_object.rect.y
            self.player_object.rect.y = self.up_viewbox
            self.shift_world(0,view_difference)

        if(self.player_object.rect.y >= self.down_viewbox):
            view_difference = self.down_viewbox - self.player_object.rect.y
            self.player_object.rect.y = self.down_viewbox
            self.shift_world(0,view_difference)
    
    def draw(self, bg,window):  #draw every object in the level
        window.blit(bg,(0,0))
        self.object_list.draw(window)
        self.monster_list.draw(window)
        self.end_block.draw(window)
        self.blood_block.draw(window)
        self.finish_block.draw(window)

class Level_1(Level): #level one
    
    def __init__(self, player_object):
        super(Level_1, self).__init__(player_object)
        level = [[2,124,365,47,"b4.png"],
                 [200,424,285,47,"b5.png"],
                 [198,408,0.5,30, None],
                 [468,360,1,1, "b1.png"],
                 [645,418,0.5,5, None],
                 [650,424,285,47,"b4.png"],
                 [935,418,0.5,5, None],
                 [1050,384,285,47,"b4.png"],
                 [1400,250,10,184,"b2.png"],
                 [1600,404,170,47,"b1.png"],
                 [1850,304,100,47,"b2.png"],
                 [2115,261,1,0.5, None],
                 [2120,271,205,47,"b3.png"],
                 [2330,261,1,0.5, None],
                 [2445,402,1,0.5, None],
                 [2450,404,285,47,"b4.png"],
                 [2725,404,285,47,"b4.png"],
                 [3000,402,1,1, None],
                 [3120,340,285,47,"b3.png"]]

        #monster lists
        monster_level = [[300,355,100,100,(150,100,50)],
                         [680,355,100,100,(150,100,50)],
                         [2280,205,100,100,(150,100,50)],
                         [2850,338,100,100,(150,100,50)]]
        #blood amount
        blood_block = [[10,10,10,10,(0,0,100)],
                       [25,10,10,10,(0,0,100)],
                       [40,10,10,10,(0,0,100)]]
            
        for block in level:     #add monsters to the group
            block = Block(block[0], block[1], block[2], block[3],block[4])
            self.object_list.add(block)
        for monster in monster_level:
            monster = Monster(monster[0],monster[1],monster[2],monster[3],monster[4])
            self.monster_list.add(monster)
            
        for blood in blood_block:   #add blood to the group
            blood = Blood(blood[0],blood[1],blood[2],blood[3],blood[4])
            self.blood_block.add(blood)
            
        self.end_block.add(Block(1, 600, 10000,0.5))
        self.finish_block.add(Block(3265, 215, 20,300, "flag.png"))

class Level_2(Level):   #level 2
    
    def __init__(self, player_object):
        super(Level_2, self).__init__(player_object)
        level = [[2,424,365,47,"b4.png"],
                 [200,424,285,47,"b5.png"],
                 [1,408,0.5,30, None],
                 [468,360,1,1, "b1.png"],
                 [645,416,0.5,5, None],
                 [650,424,285,47,"b4.png"],
                 [935,416,0.5,5, None],
                 [1050,384,285,47,"b4.png"],
                 [1500,450,10,184,"b2.png"],
                 [1650,450,170,47,"b1.png"],
                 [1850,324,100,47,"b2.png"],
                 [2115,361,1,0.5, None],
                 [2120,371,205,47,"b3.png"],
                 [2330,361,1,0.5, None],
                 [2445,402,1,0.5, None],
                 [2450,404,285,47,"b4.png"],
                 [2727,402,1,1, None],
                 [2825,404,285,47,"b4.png"],
                 [3120,340,285,47,"b3.png"]]
                 
        monster_level = [[300,355,100,100,(150,100,50)],
                         [680,355,100,100,(150,100,50)],
                         [2200,306,100,100,(150,100,50)],
                         [2550,338,100,100,(150,100,50)]]
        blood_block = [[10,10,10,10,(0,0,100)],
                       [25,10,10,10,(0,0,100)],
                       [40,10,10,10,(0,0,100)]]
            
        for block in level:
            block = Block(block[0], block[1], block[2], block[3],block[4])
            self.object_list.add(block)
        for monster in monster_level:
            monster = Monster(monster[0],monster[1],monster[2],monster[3],monster[4])
            self.monster_list.add(monster)
            
        for blood in blood_block:
            blood = Blood(blood[0],blood[1],blood[2],blood[3],blood[4])
            self.blood_block.add(blood)
            
        self.end_block.add(Block(1, 600, 10000,0.5))
        self.finish_block.add(Block(3265, 215, 20,300, "flag.png"))

#introduction to the game
class gameIntro:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Bottom Boss")
        self.screen = pygame.display.set_mode((640,480))
        self.bg = pygame.image.load("bg2.png")
        self.running = True
        self.clock = pygame.time.Clock()
        self.frames_per_second = 60
        self.music = Music('max.wav')

    def runIntro(self):     #run the function
        self.music.update()
        play = button(400,325,200,50,dimGrey)
        play.add_text("Play",white,30)
        exit_game = button(400,385,200,50,dimGrey)
        exit_game.add_text("Exit",white,30)
        
        mouse_pos = None
        click = None
        while(self.running):
            for event in pygame.event.get():
                if(event.type == pygame.QUIT)\
                or (event.type == pygame.KEYDOWN\
                and event.key == pygame.K_ESCAPE):
                    self.running = False
                    pygame.quit()
                if(event.type == pygame.MOUSEMOTION):
                    mouse_pos = pygame.mouse.get_pos()
                if(event.type == pygame.MOUSEBUTTONDOWN):
                    click = pygame.mouse.get_pressed()
           
            self.screen.blit(self.bg,(0,0))
            play.update(self.screen,mouse_pos[0],mouse_pos[1],click)
            exit_game.update(self.screen,mouse_pos[0],mouse_pos[1],click)

            if(exit_game.click == 1):
                self.running = False
                pygame.quit()
            elif(play.click == 1):
                mainGame().runGame(0)

            
            event = None
            click = None
            
            pygame.display.update()
            self.clock.tick(self.frames_per_second)
            
#main game fuction 
class mainGame:
    def __init__(self):

        pygame.init()
        pygame.display.set_caption("Bottom Boss")
        self.screen = pygame.display.set_mode((640,480))
        self.bg = pygame.image.load("background.png")
        self.running = True
        self.player = Player()
        self.clock = pygame.time.Clock()
        self.frames_per_second = 60
        
    def runGame(self,num):  #run the main fuction

        self.player.set_image("player.png")
        self.active_object_list = pygame.sprite.Group()
        self.fire_list = pygame.sprite.Group()
        self.player.set_pos(40,40)
        self.active_object_list.add(self.player)
        level_list = [Level_1(self.player), Level_2(self.player)]
        level = level_list[num]
        global  mouse_pos
        mouse_pos = None
        global click
        global event
        while(self.running):
            
            for event in pygame.event.get():

                if(event.type == pygame.QUIT)\
                or (event.type == pygame.KEYDOWN\
                and event.key == pygame.K_ESCAPE):
                    self.running = False
                    pygame.quit()
                if(event.type == pygame.MOUSEMOTION):
                    mouse_pos = pygame.mouse.get_pos()
                if(event.type == pygame.MOUSEBUTTONDOWN):
                    click = pygame.mouse.get_pressed()
            self.player.update(level.object_list,level.monster_list,
                               self.fire_list,level.end_block,
                               level.finish_block,level.blood_block, event)
            
            for monster in level.monster_list:
                monster.update(level.object_list)
            level.update()
            level.run_viewbox()
            level.draw(self.bg,self.screen)
            self.fire_list.draw(self.screen)
            self.active_object_list.draw(self.screen)
            
            if self.player.alive == 0:
                mainGame().runGame(num)
            if self.player.win == 1:
                if num >= 1:
                    gameEnd().runEnd()
                else:
                    mainGame().runGame(num+1)
            event = None
            #self.screen.blit(self.screen,(0,0))
            pygame.display.update()
            self.clock.tick(self.frames_per_second)

#button object 
class button:   
    def __init__(self,x,y,width,height,color):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.color = color
        self.click = 0
        self.click_sound = Sound("click.wav")
        
    def add_text (self,text, color, size):  #add message to the button
        myfont = pygame.font.SysFont("comicsansms", size)
        self.textSurface = myfont.render(text , 2, color)

    def check(self,mx,my, click = None):    #check if the curser is inside the botton
        if((self.x+self.w)> mx > self.x) and ((self.y+self.h)>my>self.y):
            self.color = red
            if(click != None):
                if(click[0] == 1):
                    self.click_sound.update()
                    self.click = 1
                else:
                    self.click = 0
        else:
            self.color = dimGrey
            
    def update(self,screen,eventx,eventy, click = None):    #arrae the texts to the center of the button nd display then
        if(eventx != None and eventy != None):
            self.check(eventx,eventy, click)
        pygame.draw.rect(screen,self.color,(self.x, self.y, self.w,self.h))
        self.t = self.textSurface.get_rect()
        self.t = (self.x+(self.w/3), self.y+(self.h/10))
        screen.blit(self.textSurface, self.t)

#end the game
class gameEnd:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Bottom Boss")
        self.screen = pygame.display.set_mode((640,480))
        self.bg = pygame.image.load("bb2.png")
        self.running = True
        self.clock = pygame.time.Clock()
        self.frames_per_second = 60
        self.play = button(200,150,300,100,dimGrey)
        self.play.add_text("Play Again",white,30)
        self.exit_game = button(200,350,300,100,dimGrey)
        self.exit_game.add_text("Exit",white,30)

    def runEnd(self):
        
            self.screen.blit(self.bg,(0,0))
            pygame.display.update()
            pygame.time.wait(4000)         #wait for 5 seconds and then automatically quit
            pygame.quit()
            sys.exit(1)

class Sound:    #play the sound
    def __init__(self,sound):
        self.sound = pygame.mixer.Sound(sound)
    def update(self):
        self.sound.play()
        
class Music:    #play the music
    def __init__(self,sound):
        self.music = pygame.mixer.Sound(sound)
    def update(self):
        self.music.play()

gameIntro().runIntro()

