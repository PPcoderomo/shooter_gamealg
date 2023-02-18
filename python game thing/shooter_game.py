from pygame import *
from random import randint
from time import time as timer
window = display.set_mode((700, 500))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
mixer.init()
mixer.music.load('space.ogg')
font.init()
global loss ,hit ,test_lose ,test_win
font1 = font = font.SysFont('Arial', 36)
loss = 0
hit = 0
num_fire = 0
rel_time = False
test_lose = font1.render(
    "Missed: " + str(loss), 1, (255,255,255)
)
test_win = font1.render(
    "Hit: " + str(hit), 1, (255,255,255)
)
mixer.music.play()
#kick = mixer.Sound('kick.ogg')
game = True
clock = time.Clock()
FPS = 60

class GameSprite(sprite.Sprite):
    def __init__(self, filename, speed, x, y, size_x = 65, size_y = 65):
        super().__init__ ()
        self.image = transform.scale(image.load(filename),(size_x,size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x >= 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x <= 635:
            self.rect.x += self.speed
    def fire(self):
        bullet =Bullet("bullet.png", 15, self.rect.centerx, self.rect.top, 10, 20)
        bullets.add(bullet)
class Bullet(GameSprite):
    def update(self):
        self.rect.y-=self.speed
        if self.rect.y < 0:
            self.kill()
class Enemy(GameSprite):
    def update(self):
        global loss, test_lose 
        self.rect.y += self.speed  
        if self.rect.y >= 500:
            self.rect.y = -50
            self.rect.x = randint(0,635)   
            loss = loss + 1  
            test_lose = font1.render("Missed: " + str(loss), 1, (255,255,0))  
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed  
        if self.rect.y >= 500:
            self.rect.y = -50
            self.rect.x = randint(0,635)      
hero = Player("rocket.png", 5, 20, 435)
bullets = sprite.Group()
UFOs = sprite.Group()
meteors = sprite.Group()
for i in range(3):
    meteor = Asteroid("asteroid.png", randint(1,2), randint(0, 635), -50)
    meteors.add(meteor)
for i in range(6):
    UFO = Enemy("ufo.png", randint(1,2), randint(0, 635), -50)
    UFOs.add(UFO)
finish = False

while game:
    if finish != True:
        window.blit(background,(0, 0))
        window.blit(test_lose, (1,25))
        window.blit(test_win,(1,1))
        hero.reset()
        hero.update() 
        bullets.draw(window)
        bullets.update()
        UFOs.draw(window)
        UFOs.update()
        meteors.draw(window)
        meteors.update()
        if rel_time == True:
            cur_time2 = timer()
            if cur_time2 - cur_time < 3:
                reload_gun = font1.render("reloading", 1, (200,0,200))
                window.blit(reload_gun,(310,220))
            else:
                num_fire = 0
                rel_time = False
        if sprite.spritecollide(hero, meteors, False):
            finish = True
            fin = font1.render("YOU LOSE", 1, (200,0,0))
            window.blit(fin,(310,220))
        sprites_list = sprite.groupcollide(UFOs, bullets, True, True)
        for i in sprites_list:
            hit = hit + 1
            UFO = Enemy("ufo.png", randint(1,2), randint(0, 635), -50)
            UFOs.add(UFO)
            test_win = font1.render(
            "Hit: " + str(hit), 1, (255,0,255))
        if hit >= 15:
            finish = True
            fin = font1.render("YOU WIN", 1, (0,200,0))
            window.blit(fin,(310,220))
        if loss >= 5:
            finish = True
            fin = font1.render("YOU LOSE", 1, (200,0,0))
            window.blit(fin,(310,220))
        display.update()
        clock.tick(FPS)
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 4 and rel_time == False:
                    hero.fire()
                    num_fire = num_fire + 1
                if num_fire > 4 and rel_time == False:
                    rel_time = True
                    cur_time = timer()
