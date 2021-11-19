# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 20:10:53 2019

@author: zbin13
"""

import pygame
from scoreboard import Scoreboard
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from music_button import Music_Button
from music_button_ingame import Music_Button_Ingame
from ship import Ship
#from alien import Alien
import game_functions as gf


def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    
    ai_settings = Settings()
    screen = pygame.display.set_mode(
            (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    #创建Play按钮
    play_button = Button(ai_settings, screen, "Play")

    #创建音乐播放按钮
    play_music_button = Music_Button(ai_settings, screen, "Music")
    play_music_ingame = Music_Button_Ingame(ai_settings, screen, 'Music')
    
    #播放音乐
    gf.check_play_music(stats)
    # 设置背景色
    #bg_color = (230,230,230)
    
    #创建一艘飞船、一个子弹编组、一个外星人编组和一个外星人子弹编组
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    alienBullets = Group()
    bosses = Group()
    
    #开始游戏的主循环
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, play_music_button, 
                        play_music_ingame, ship, aliens, bullets, alienBullets, bosses)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets,alienBullets, bosses)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets, alienBullets, bosses)
            
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, alienBullets, bosses,
                         play_button, play_music_button, play_music_ingame)

run_game()

