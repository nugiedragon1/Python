import pygame
import random

class Player(pygame.sprite.Sprite):                                     #THIS CLASS PUT THE PLAYER IMAGE,HIT BOX COLOR AND FITTING THE PLAYER's IMAGE HITBOX SO IT FIT WITHIN THE IMAGE
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.image.load("ironman3.png").convert_alpha()

        self.image.set_colorkey((255,255,255))
        # self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image,(60,80))
        self.image.set_colorkey((255,255,255))
        self.rect.x, self.rect.y = (self.game.widht/2, self.game.height-2*50)
        self.mask=pygame.mask.from_surface(self.image)


class UFO(pygame.sprite.Sprite):                                    #CLASS FOR UFO THAT SHOOTS RANDOM BULLETS
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ufo2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image,(800,80))

class Enemy(pygame.sprite.Sprite):                      #CLASS FOR BULLETS
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((10,40),pygame.SRCALPHA)
        self.image.fill((0,0,255))
        # self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        # self.image = pygame.transform.scale(self.image,(30,30))

        self.rect.x, self.rect.y = (x, y)
        self.mask=pygame.mask.from_surface(self.image)
        self.speed = 1
    def update(self):
        # if self.game.score < 15:
        #     self.speed = 5
        # elif self.game.score < 20:
        #     self.speed = 8
        # elif self.game.score < 50:
        #     self.speed = 12
        # elif self.game.score < 80:
        #     self.speed = 15
        # else:
        #     self.speed = 25
        self.rect.y += self.speed

        if self.rect.y > self.game.height + 50:
            self.game.score += 1
            self.kill()


class Game:                                         #THIS CLASS INCLUDE ALL THE GAME MECHANICS SUCH AS BACKGROUND,SCORE,CONTROL,MENU,LOOPS.
    def __init__(self):
        pygame.init()
        self.widht = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.widht, self.height))
        self.screen.fill((0,0,0))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 35)
        self.run = True
        self.play = False

        self.game_over = False
        self.score = 0
        self.health = 75
    def draw_score(self):
        font = pygame.font.SysFont('arial.ttf',46)
        text_surface= font.render('Score: {}'.format(self.score),True,(250,250,210))
        self.screen.blit(text_surface,(500,500))
    def menu(self):
        run = True
        while run:
            self.bg=pygame.Surface((800,600))
            self.bg.fill((0,0,0))
            self.rect=self.bg.get_rect()
            self.screen.blit(self.bg,self.rect)
            self.button=pygame.Surface((300,100))
            self.button.fill((255,0,0))
            self.rect=self.button.get_rect()
            self.rect.center = (400,300)
            self.screen.blit(self.button,self.rect)
            font=pygame.font.SysFont('arial.ttf',46)
            text_surface = font.render('ENTER TO ROLL',True,(255,255,255))
            self.rect=text_surface.get_rect()
            self.rect.center = (400,300)
            self.screen.blit(text_surface,self.rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        run = False
                        self.play = True
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        self.run = False
            pygame.display.flip()

    def lose(self):
        run = True
        while run:
            self.bg=pygame.Surface((800,600))
            self.bg.fill((0,0,0))
            self.rect=self.bg.get_rect()
            self.screen.blit(self.bg,self.rect)
            # self.button=pygame.Surface((200,100))
            # self.button.fill((255,0,0))
            # self.rect=self.button.get_rect()
            # self.rect.center = (400,300)
            # self.screen.blit(self.button,self.rect)
            font=pygame.font.SysFont('arial.ttf',120)
            text_surface = font.render('YOU DIED',True,(255,0,0))
            self.rect=text_surface.get_rect()
            self.rect.center = (400,300)
            self.screen.blit(text_surface,self.rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.play = False
                    self.run = False
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.play = False
                        run = False
                        pygame.mixer.music.stop()
            pygame.display.flip()

    def new_game(self):                 #CALL ALL THE GAME INTERFACES
        self.health = 75
        self.player = Player(self)
        self.all_sprites = pygame.sprite.Group(self.player)
        self.enemies = pygame.sprite.Group()
        self.ufo = UFO()
        self.all_sprites.add(self.ufo)
        self.bg = pygame.image.load("bekgron.jpg").convert()
        self.bg = pygame.transform.scale(self.bg,(800,600))
        pygame.mixer.music.load('themesong.mp3')
        pygame.mixer.music.play()

    def control(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.play = False
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.play = False
                    pygame.mixer.music.stop()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if not self.player.rect.x<10:
                self.player.rect.x -= 1
        if keys[pygame.K_RIGHT]:
            if not self.player.rect.x>740:
                 self.player.rect.x += 1
        if keys[pygame.K_UP]:
            if not self.player.rect.y<10:
                self.player.rect.y -= 1
        if keys[pygame.K_DOWN]:
            if not self.player.rect.y>540:
                 self.player.rect.y += 1

    def update(self):                                       #DRAW ALL THE GAME INTERFACES
        self.screen.blit(self.bg,(0,0))
        self.healthbar = pygame.Surface((self.health,10),pygame.SRCALPHA)
        self.healthbar.fill((255,0,255))
        self.screen.blit(self.healthbar,self.player.rect)
        self.draw_score()
        self.delay = random.random()
#        self.screen.blit("bekgron.jpg",(0,0))
        if len(self.enemies) < 50 and self.delay < 0.1:
            e = Enemy(self, random.randint(0,800), 100)
            self.all_sprites.add(e)
            self.enemies.add(e)
        hit = pygame.sprite.spritecollide(self.player , self.enemies,True,pygame.sprite.collide_mask)
        if hit :
            self.health -= 1
        if self.health == 0:
            self.lose()
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        pygame.display.update()


g = Game()
while g.run:
    g.menu()
    g.new_game()
    while g.play:
        g.control()
        g.update()
pygame.quit()
