# Разработай свою игру в этом файле!
from pygame import *
class GameSprite(sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        sprite.Sprite.__init__(self)
        self.image=transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def __init__(self, picture, w, h, x, y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, picture, w, h, x, y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    def update(self):
        self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet('пуля.jpg', 15, 20, self.rect.right, self.rect.centery, 10)
        bullets.add(bullet)

class Enemy(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    def update(self):
        if self.rect.x <= 420:
            self.side = "right"
        if self.rect.x >= 700 - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    def update(self):
        self.rect.x += self.speed   
        if self.rect.x > 700+10:
            self.kill()

wall_1 = GameSprite('фон.jpg', 80, 180, 200, 250)

barriers = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()

player = Player('кот.jpg', 80, 80, 5, 50, 0, 0)
final = GameSprite('win.jpg', 120, 80, 560, 400)
monster1 = Enemy('враг.jpg', 80, 150, 80, 80, 5)
# monster2 = Enemy('враг.jpg', 80, 230, 80, 80, 5)

barriers.add(wall_1)
monsters.add(monster1)
# monsters.add(monster2)

win = transform.scale(image.load('хлопушка.png'), (700, 500))
window = display.set_mode((700, 500))
display.set_caption('Моя первая игра')
a = (255, 212, 94)
b = (235, 64, 52)
font.init()
font = font.SysFont('Arial', 30)
win1 = font.render('YOU WIN!', True, b)
finish = False

run = True
while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                player.x_speed = -5
            elif e.key == K_RIGHT:
                player.x_speed = 5
            elif e.key == K_UP:
                player.y_speed = -5
            elif e.key == K_DOWN:
                player.y_speed = 5
            elif e.key == K_SPACE:
                player.fire()    

        elif e.type == KEYUP:
            if e.key == K_LEFT:
                player.x_speed = 0
            elif e.key == K_RIGHT:
                player.x_speed = 0
            elif e.key == K_UP:
                player.y_speed = 0
            elif e.key == K_DOWN:
                player.y_speed = 0

    if finish != True:
        window.fill(a)
        player.update()
        bullets.update()
        
        player.reset()
        bullets.draw(window)
        barriers.draw(window)
        final.reset()
        wall_1.reset()

        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)

        if sprite.spritecollide(player, monsters, False):
            finish = True
            img = image.load('проигрыш.jpg')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (500 * d, 500)), (90, 0))

        if sprite.collide_rect(player, final):
            finish = True
            img = image.load('хлопушка.png')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (700, 500)), (0, 0))
          
        display.update()
display.update()