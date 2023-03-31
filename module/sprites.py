import pygame
import math
import data
import random
time_anim = data.TIME_ANIM

class Hero(pygame.Rect):
    def __init__(self, x, y, width, height, img, recharge=40, step=2.5, distance=250):
        super().__init__(x, y, width, height)
        self.center = (data.settings_window['WIDTH']//2, data.settings_window['HEIGHT']//2)
        self.STEP = step

        self.IMAGES = img
        self.IMAGE = None

        self.INDEX_ANIM = 0
        self.TIME_ANIM = 30

        self.ROT = 0
        self.RECHARGE = recharge
        self.RECHARGE_TIME = recharge - 1

        self.LEVEL = 1
        self.EXP = 0
        self.MAX_EXP = 100
        self.HP = 100
        self.HP_MAX = 100
        self.FONT_LEVEL = pygame.font.SysFont('rubik', 34)

        self.DAMAGE = 25
        self.DISTANCE = distance
        self.BULLETS = 1

    def draw(self, window):
        # (self.INDEX_ANIM, len(self.IMAGES))
        #print(self.ROT)
        window.blit(self.IMAGE, (self.x, self.y))
        #pygame.draw.line(window, (255, 0, 0), self.center, (self.x + 900 * math.cos(self.ROT), self.y + 900 * math. sin(self.ROT)), 2)
        size_rect_exp = data.settings_window['WIDTH']//self.MAX_EXP*self.EXP
        rect_exp = pygame.Rect(0, 0, size_rect_exp, 5)
        pygame.draw.rect(window, data.state_color['exp'], rect_exp)

        render_level = self.FONT_LEVEL.render(f'{self.LEVEL}', True, data.state_color['exp'])
        rect_level = render_level.get_rect(centerx=data.settings_window['WIDTH']//2, top=7).topleft
        window.blit(render_level, rect_level)

        size_rect_hp = self.width/self.HP_MAX*self.HP
        rect_hp = pygame.Rect(self.x, self.y-5, size_rect_hp, 5)
        rect_hp0 = pygame.Rect(self.x-1, self.y-6, self.width+2, 6)
        pygame.draw.rect(window, data.state_color['hp'][0], rect_hp)
        pygame.draw.rect(window, data.state_color['hp'][1], rect_hp0, 1)


    def move(self, objects):
        mouse_pos = pygame.mouse.get_pos()
        dx = mouse_pos[0] - self.centerx
        dy = mouse_pos[1] - self.centery
        
        self.ROT = math.atan2(dy, dx)
        #print(self.ROT)

        keys = pygame.key.get_pressed()

        if self.TIME_ANIM > time_anim:
            self.TIME_ANIM = 0
        if True in [keys[pygame.K_w], keys[pygame.K_s]] and self.TIME_ANIM <= time_anim:
            self.TIME_ANIM += 1

        if self.TIME_ANIM <= time_anim//2:
            self.INDEX_ANIM = 1
        else:
            self.INDEX_ANIM = 2

        if not True in [keys[pygame.K_w], keys[pygame.K_s]]:
            if self.ROT >= -1.5 and self.ROT <= 1.5:
               self.IMAGE = self.IMAGES['right'][0]
            else:
                self.IMAGE = self.IMAGES['left'][0]
        elif True in [keys[pygame.K_w], keys[pygame.K_s]]:
            if self.ROT >= -1.5 and self.ROT <= 1.5:
               self.IMAGE = self.IMAGES['right'][self.INDEX_ANIM]
            else:
                self.IMAGE = self.IMAGES['left'][self.INDEX_ANIM]

        if keys[pygame.K_w]:
            for object_ in objects:
                object_.centerx -= math.cos(self.ROT) * self.STEP
                object_.centery -= math.sin(self.ROT) * self.STEP
        if keys[pygame.K_s]:
            for object_ in objects:
                object_.centerx += math.cos(self.ROT) * self.STEP
                object_.centery += math.sin(self.ROT) * self.STEP

    def shot(self, bullets):
        keys = pygame.key.get_pressed()

        self.RECHARGE_TIME += 1
        if self.RECHARGE_TIME >= self.RECHARGE and keys[pygame.K_q] == True:
            if self.BULLETS == 1:
                bullets.append(Bullet(self.x-5, self.y-5, 10, 10, self.ROT, data.img_bullet_player, self.DAMAGE, self.DISTANCE))
            else:
                for i in range((self.BULLETS-1)*-1, (self.BULLETS-1)*1, 1):
                    bullets.append(Bullet(self.x-5, self.y-5, 10, 10, self.ROT+(i/10), data.img_bullet_player, self.DAMAGE, self.DISTANCE))
            bullets[-1].center = self.center
            self.RECHARGE_TIME = 0

class Bullet(pygame.Rect):
    def __init__(self, x, y, width, height, rot, img, damage=25, distance=250, type_='hero', step=5):
        super().__init__(x, y, width, height)
        self.STEP = step
        self.ROT = rot
        self.DAMAGE = damage
        self.TYPE = type_
        self.IMG = img

        self.DISTANCE = distance
        self.DISTANCE_TRAV = 0

    def draw(self, window):
        window.blit(self.IMG, self.topleft)
        #pygame.draw.rect(window, (200, 200, 200), self)

    def move(self, bullets):
        self.x += math.cos(self.ROT) * self.STEP
        self.y += math.sin(self.ROT) * self.STEP
        self.DISTANCE_TRAV += ((math.cos(self.ROT) * self.STEP)**2+(math.sin(self.ROT) * self.STEP)**2)**0.5
        if self.DISTANCE_TRAV >= self.DISTANCE:
            bullets.remove(self)

    def attack(self, enemes, hero, bullets, drops):
        if self.TYPE == 'hero':
            remove = False
            for i in self.collidelistall(enemes):
            #    self.STEP = -self.STEP
                if i >= len(enemes):
                    break
                enemes[i].HP -= self.DAMAGE
                if enemes[i].HP <= 0:
                    enemes[i].deth(enemes, drops)
                remove = True
            if remove:
                try:
                    bullets.remove(self)
                except:
                    pass

class Eneme(pygame.Rect):
    def __init__(self, x, y, width, height, level=1, step=1, imgs=data.enemy_imgs,):
        super().__init__(x, y, width, height)

        self.LEVEL = level
        self.STEP = step + self.LEVEL * step//10
        self.DAMAGE = self.LEVEL*50
        self.IMGS = imgs

        self.MAX_HP = self.LEVEL * 50
        self.HP = self.MAX_HP

        self.INDEX_ANIM = 0
        self.TIME_ANIM = 30

    def draw(self, window):
        window.blit(self.IMGS[self.INDEX_ANIM], self.topleft)
        #pygame.draw.rect(window, (60, 200, 80), self)

    def move(self, coord_hero):
        dx = coord_hero[0] - self.centerx
        dy = coord_hero[1] - self.centery
        rot = math.atan2(dy, dx)

        self.x += math.cos(rot) * self.STEP
        self.y += math.sin(rot) * self.STEP
        
        #if coord_hero[0] >= self.centerx:
        #    self.centerx += self.STEP
        #elif coord_hero[0] <= self.centerx:
        #    self.centerx -= self.STEP

        #if coord_hero[1] >= self.centery:
        #    self.centery += self.STEP
        #elif coord_hero[1] <= self.centery:
        #    self.centery -= self.STEP

        if self.TIME_ANIM > time_anim:
            self.TIME_ANIM = 0
        self.TIME_ANIM += 1

        if self.TIME_ANIM <= time_anim//2:
            self.INDEX_ANIM = 0
        else:
            self.INDEX_ANIM = 1

    def attack(self, hero, enemes):
        if self.colliderect(hero):
            hero.HP -= self.DAMAGE
            enemes.remove(self)

    def deth(self, enemes, drops):
        if random.randint(1, 10) == 1:
            drops.append(Drop(self.centerx, self.centery, 8, 8, data.imgs_drop[1], 'hp', self.LEVEL))
        elif random.randint(1, 1) == 1:
            drops.append(Drop(self.centerx, self.centery, 8, 8, data.imgs_drop[0], level=self.LEVEL))
        enemes.remove(self)

class Drop(pygame.Rect):
    def __init__(self, x, y, width, height, img, type_='exp', level=1):
        super().__init__(x, y, width, height)

        self.LEVEL = level
        self.TYPE = type_
        self.IMG = img

    def draw(self, window):
        window.blit(self.IMG, self.topleft)

    def up_hpexp(self, hero, drops):
        if self.colliderect(hero):
            if self.TYPE == 'exp':
                hero.EXP += self.LEVEL*20
            elif self.TYPE == 'hp':
                hero.HP += self.LEVEL*10
                if hero.HP > hero.HP_MAX:
                    hero.HP = hero.HP_MAX
            drops.remove(self)
