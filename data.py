import pygame
pygame.init()

settings_window = {
    'WIDTH' : 900,
    'HEIGHT' : 650,
    'FPS' : 50
    }

menu_color = {
    'color_text_title' : (86, 86, 120),
    'menu_fon' : (20, 40, 50),
    'button_color' : (56, 56, 100),
    'color_text_button' : (20, 20, 30)
}

game_color = {
    'fon' : (70, 70, 70)
}

state_color = {
    'exp' : (90, 90, 250),
    'hp' : ((250, 33, 33), (150, 33, 33))
}

TIME_ANIM = 30

def load_img(part_name, folder, l):
    path_img = f'img//'

    if l[0] != 0:
        ans = {}
        for el in l:
            l_img = []

            l_img.append(pygame.image.load(path_img+f'{part_name}_{el}.png'))

            for i in range(2):
                l_img.append(pygame.image.load(path_img+f'{part_name}_{el}_{i}.png'))

            ans[el] = l_img

    else:
        ans = []
        for el in l:
            ans.append(pygame.image.load(path_img+f'{part_name}_{el}.png'))
    return ans

player_imgs = load_img('player', 'player', ['right', 'left'])
enemy_imgs = load_img('enemy', 'enemy', [0, 1])
#print(player_imgs)
imgs_drop = (pygame.transform.scale(pygame.image.load('img/Sprite-00011.png'), (8, 8)), pygame.transform.scale(pygame.image.load('img/Sprite-00012.png'), (8, 8)))
img_play = pygame.image.load('img/play.png')
img_bullet_player = pygame.image.load('img/bullet_player.png')
cursor_img = pygame.image.load('img/pricel.png')
icon = pygame.image.load('img/icon.ico')
