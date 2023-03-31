import pygame
import module.sprites as sprites
import module.menu as menu
import data
import time
import random

pygame.init()

width, height = data.settings_window['WIDTH'], data.settings_window['HEIGHT']
FPS = data.settings_window['FPS']
clock = pygame.time.Clock()

window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Hero survival')
pygame.display.set_icon(data.icon)

def play_b():
    global menu_regim
    menu_regim = 1
    global start_time_game
    start_time_game = time.time() 

def up_hp(hero):
    global menu_regim
    hero.HP_MAX += hero.HP_MAX // 2
    hero.HP = hero.HP_MAX
    menu_regim = 1

def up_damage(hero):
    global menu_regim
    hero.DAMAGE += hero.DAMAGE // 3
    menu_regim = 1

def up_recharge(hero):
    global menu_regim
    hero.RECHARGE -= hero.RECHARGE / 10
    menu_regim = 1

def up_distance(hero):
    global menu_regim
    hero.DISTANCE += hero.DISTANCE / 20
    menu_regim = 1

def up_speed(hero):
    global menu_regim
    hero.STEP += hero.STEP / 50
    menu_regim = 1

def up_numbullets(hero):
    global menu_regim
    hero.BULLETS += 1
    menu_regim = 1

def resume_b():
    global menu_regim
    menu_regim = 1

def restart_b():
    global menu_regim
    menu_regim = 1
    return True

def main_menu_b():
    global menu_regim
    menu_regim = 0

main_menu = menu.Menu(window, 'Hero survival', 150, data.menu_color['color_text_title'], data.menu_color['menu_fon'])
main_menu.add_button((400, 100), 'Play', play_b, 80, data.menu_color['button_color'], data.menu_color['color_text_button'], data.img_play)

levelup_menu = menu.Menu(window, 'LEVEL UP', 150, data.menu_color['color_text_title'], None)

pause_menu = menu.Menu(window, 'Pause', 150, data.menu_color['color_text_title'], None)
pause_menu.add_button((400, 100), 'Resume', resume_b, 80, data.menu_color['button_color'], data.menu_color['color_text_button'])
pause_menu.add_button((400, 100), 'Restart', restart_b, 80, data.menu_color['button_color'], data.menu_color['color_text_button'])

game_over_menu = menu.Menu(window, 'Game Over', 150, data.menu_color['color_text_title'], None)
game_over_menu.add_button((400, 100), 'Main Menu', main_menu_b, 80, data.menu_color['button_color'], data.menu_color['color_text_button'])
game_over_menu.add_button((400, 100), 'Restart', restart_b, 80, data.menu_color['button_color'], data.menu_color['color_text_button'])

font_timer = pygame.font.SysFont('sourceserifproblack', 50)
start_time_game = 0

def run():
    game = True
    global menu_regim
    menu_regim = 0
    hero = sprites.Hero(450, 325, 40, 40, data.player_imgs)
    enemes = [sprites.Eneme(0, 0, 20, 20), sprites.Eneme(data.settings_window['WIDTH'], data.settings_window['HEIGHT'], 20, 20)]
    bullets = []
    drops = []
    current_enemy_time = 0
    time_delay = 0
    start_time_game = time.time()

    while game:
        if menu_regim == 2 or menu_regim == 3 or menu_regim == 4:
            hero.draw(window)

            for eneme in enemes:
                    eneme.draw(window)

            for bullet in bullets:
                bullet.draw(window)
                
        if menu_regim == 0:
            pygame.mouse.set_visible(True)
            main_menu.show()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in main_menu.BUTTONS:
                        if button[0].collidepoint(pygame.mouse.get_pos()):
                            button[-2]()

        elif menu_regim == 1:
            pygame.mouse.set_visible(False)
            window.fill(data.game_color['fon'])
            window.blit(data.cursor_img, (pygame.mouse.get_pos()[0]-4, pygame.mouse.get_pos()[1]-4))
            if not hero.EXP >= hero.MAX_EXP:
                time_timer = time.time() - start_time_game + time_delay
                window.blit(font_timer.render(f'{int(time_timer//60)}:{int(time_timer-(time_timer//60*60))}', True, (200, 200, 200)), (5, 5))

                for eneme in enemes:
                    eneme.draw(window)
                    eneme.attack(hero, enemes)
                    eneme.move(hero.center)

                for bullet in bullets:
                        bullet.draw(window)
                        bullet.move(bullets)
                        bullet.attack(enemes, hero, bullets, drops)

                if int(time_timer) - int(current_enemy_time) == 15:
                    current_enemy_time = time_timer
                    for i in range(int(time_timer%60//5)):
                        if random.randint(1, 2) == 1:
                            if random.randint(1, 2) == 1:
                                enemes.append(sprites.Eneme(random.randint(0, data.settings_window['WIDTH']), 0, 20, 20, time_timer//60+1, 1))
                            else:
                                enemes.append(sprites.Eneme(random.randint(0, data.settings_window['WIDTH']), data.settings_window['HEIGHT'], 20, 20, time_timer//60+1, 1))
                        else:
                            if random.randint(1, 2) == 1:
                                enemes.append(sprites.Eneme(0, random.randint(0, data.settings_window['HEIGHT']), 20, 20, time_timer//60+1, 1))
                            else:
                                enemes.append(sprites.Eneme(data.settings_window['WIDTH'], random.randint(0, data.settings_window['HEIGHT']), 20, 20, time_timer//60+1, 1))
                
                hero.move(enemes+bullets+drops)
                hero.draw(window)
                hero.shot(bullets)

                for drop in drops:
                    drop.draw(window)
                    drop.up_hpexp(hero, drops)

                if hero.HP <= 0:
                    menu_regim = 4

            else:
                hero.LEVEL += 1
                hero.EXP -= hero.MAX_EXP
                hero.MAX_EXP += hero.MAX_EXP // 2
                #'hp', 'damage', 'recharge', 'distance', 'speed', 'numbullets'
                menu_regim = 2
                upgrates_list = ['hp', 'damage', 'recharge', 'distance', 'speed', 'numbullets']
                upgrate_list = []
                for i in range(3):
                    index = random.randint(0, len(upgrates_list)-1)
                    upgrate_list.append(upgrates_list[index])
                    upgrates_list.remove(upgrates_list[index])
                levelup_menu.BUTTONS = []
                if 'hp' in upgrate_list:
                    levelup_menu.add_button((250, 70), 'hp',  up_hp, 50, data.menu_color['button_color'], data.menu_color['color_text_button'])
                if 'damage' in upgrate_list:
                    levelup_menu.add_button((250, 70), 'damage',  up_damage, 50, data.menu_color['button_color'], data.menu_color['color_text_button'])
                if 'recharge' in upgrate_list:
                    levelup_menu.add_button((250, 70), 'recharge',  up_recharge, 50, data.menu_color['button_color'], data.menu_color['color_text_button'])
                if 'distance' in upgrate_list:
                    levelup_menu.add_button((250, 70), 'distance',  up_distance, 50, data.menu_color['button_color'], data.menu_color['color_text_button'])
                if 'speed' in upgrate_list:
                    levelup_menu.add_button((250, 70), 'speed',  up_speed, 50, data.menu_color['button_color'], data.menu_color['color_text_button'])
                if 'numbullets' in upgrate_list:
                    levelup_menu.add_button((250, 70), '№ bullets',  up_numbullets, 50, data.menu_color['button_color'], data.menu_color['color_text_button'])
                time_delay = time_timer
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        enemes.append(sprites.Eneme(0, 0, 20, 20))
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu_regim = 3
                        time_delay = time_timer

        elif menu_regim == 2:
            pygame.mouse.set_visible(True)
            levelup_menu.show()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button in levelup_menu.BUTTONS:
                            if button[0].collidepoint(pygame.mouse.get_pos()):
                                button[-2](hero)
                                start_time_game = time.time()

        elif menu_regim == 3:
            pygame.mouse.set_visible(True)
            pause_menu.show()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button in pause_menu.BUTTONS:
                            if button[0].collidepoint(pygame.mouse.get_pos()):
                                if button[-2]():
                                    hero = sprites.Hero(450, 325, 40, 40, data.player_imgs)
                                    enemes = [sprites.Eneme(0, 0, 20, 20), sprites.Eneme(data.settings_window['WIDTH'], data.settings_window['HEIGHT'], 20, 20)]
                                    bullets = []
                                    drops = []
                                    current_enemy_time = 0
                                    time_delay = 0
                                start_time_game = time.time()

        elif menu_regim == 4:
            pygame.mouse.set_visible(True)
            game_over_menu.show()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button in game_over_menu.BUTTONS:
                            if button[0].collidepoint(pygame.mouse.get_pos()):
                                button[-2]()
                                hero = sprites.Hero(450, 325, 40, 40, data.player_imgs)
                                enemes = [sprites.Eneme(0, 0, 20, 20), sprites.Eneme(data.settings_window['WIDTH'], data.settings_window['HEIGHT'], 20, 20)]
                                bullets = []
                                drops = []
                                current_enemy_time = 0
                                time_delay = 0
                                start_time_game = time.time()

        pygame.display.flip()
        clock.tick(FPS)

run()
