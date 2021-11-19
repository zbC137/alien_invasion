# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 21:05:44 2019

@author: zbin13
"""

import sys
from time import sleep

import pygame
import random
from bullet import Bullet
from alien import Alien
from alien_bullet import AlienBullet
from boss import Boss

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
        
def fire_bullet(ai_settings, screen, ship, bullets):
    """如果还没有达到限制，就发射一颗子弹"""
    #创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        
def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False
        
def check_events(ai_settings, screen, stats, sb, play_button, play_music_button, 
                 play_music_ingame, ship, aliens, bullets, alienBullets, bosses):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
                
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                              aliens, bosses, bullets, alienBullets, mouse_x, mouse_y)
            check_play_music_button(ai_settings, screen, stats, play_music_button,
                                    play_music_ingame, mouse_x, mouse_y)

def check_play_music(stats):
    if stats.play_music:
        #添加背景音乐
        pygame.mixer.init()
        pygame.mixer.music.load('images/aibgm.wav')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1, 0)
    elif not stats.play_music:
        pygame.mixer.music.stop()

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bosses, 
                      bullets, alienBullets, mouse_x, mouse_y):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()

        #隐藏光标
        #pygame.mouse.set_visible(False)

        #重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        #重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        alienBullets.empty()
        bosses.empty()

        #创建新的外星人，并让飞船居中
        create_alien(ai_settings, screen, aliens)
        ship.center_ship()

def check_play_music_button(ai_settings, screen, stats, play_music_button, play_music_ingame, mouse_x, mouse_y):
    """在玩家单击stop music时停止背景音乐"""
    #游戏开始前的检测
    button_clicked = play_music_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and stats.play_music:
        pygame.mixer.music.stop()
        stats.play_music = False
    elif button_clicked and not stats.play_music:
        pygame.mixer.music.play(-1, 0)
        stats.play_music = True

    #游戏开始后的检测
    button_clicked_ingame = play_music_ingame.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked_ingame and stats.play_music:
        pygame.mixer.music.stop()
        stats.play_music = False
    elif button_clicked_ingame and not stats.play_music:
        pygame.mixer.music.play(-1, 0)
        stats.play_music = True

            
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, alienBullets, bosses,
                  play_button, play_music_button,play_music_ingame):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color) #背景色
    
    if stats.game_active:
        #在飞船和外星人后面重绘所有子弹
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        ship.blitme()
        #alien.blitme()
        aliens.draw(screen)
        for alienBullet in alienBullets.sprites():
            alienBullet.draw_alienBullet()

        bosses.draw(screen)

        #显示得分
        sb.show_score()
        
        #绘制音乐按钮
        play_music_ingame.draw_button()
        
    #如果游戏处于非活动状态，就绘制Play和Stop music按钮
    if not stats.game_active:
        play_button.draw_button()
        play_music_button.draw_button()

    #让最近绘制的屏幕可见
    pygame.display.flip()
    
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alienBullets, bosses):
    """更新子弹的位置，并删除已消失的子弹"""
    bullets.update()
        
    #删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, 
                                  bullets, alienBullets,bosses)
    check_bullet_boss_collisions(ai_settings, screen, stats, sb, ship, 
                                     aliens, bullets, alienBullets, bosses)

    alienBullets.update()

    for alienBullet in alienBullets.copy():
        if alienBullet.rect.top >= ai_settings.screen_height:
            alienBullets.remove(alienBullet)
    
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, 
                                  ship, aliens, bullets, alienBullets, bosses):
    """响应子弹和外星人的碰撞"""
    #检查是否有子弹击中了外星人
    #如果是这样，就删除相应的子弹和外星人,并更新需要消除的外星人数目
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens1 in collisions.values():
            stats.score += ai_settings.alien_points*len(aliens1)
            sb.prep_score()
            stats.aims -= len(aliens1)
        check_high_score(stats, sb)
    
    if stats.aims == 0:
        #创建一个通关boss
        create_boss(ai_settings, screen, bosses)
        stats.aims -= 1
        

def create_boss(ai_settings, screen, bosses):
    """创建一个boss并将其放在屏幕顶部随机位置"""
    boss = Boss(ai_settings, screen)
    boss_width = boss.rect.width
    boss.x = round(random.randint(0,ai_settings.screen_width - boss_width))
    boss.rect.x = boss.x
    boss.rect.y = 0
    bosses.add(boss)

def check_bullet_boss_collisions(ai_settings, screen, stats, sb, ship, 
                                     aliens, bullets, alienBullets, bosses):
    """响应子弹与boss的碰撞"""
    collisions = pygame.sprite.groupcollide(bosses, bullets, False, True)

    if collisions:
        for bullets1 in collisions.values():
            stats.kill_boss -= len(bullets1)

    if stats.kill_boss <= 0:
        stats.score += ai_settings.boss_points
        sb.prep_score()
        check_high_score(stats, sb)

        #删除现有的子弹并新建外星人
        bullets.empty()
        aliens.empty()
        alienBullets.empty()
        bosses.empty()
        ai_settings.increase_speed()

        #提高等级
        stats.level += 1
        stats.aims = 10 + 5*stats.level
        stats.kill_boss = 2*stats.level
        sb.prep_level()

        sleep(1)

        create_alien(ai_settings, screen, aliens)
        #create_alienbullets(ai_settings, screen, aliens, alienBullets)
        ship.center_ship()

def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def create_alien(ai_settings, screen, aliens):
    """创建一个外星人并将其放在屏幕顶部随机位置"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = round(random.randint(0,ai_settings.screen_width - alien_width))
    alien.rect.x = alien.x
    alien.rect.y = 0
    aliens.add(alien)

def create_alienbullets(ai_settings, screen, aliens, alienBullets):
    """让外星人发射子弹"""
    for alien in aliens:
        new_alienbullet = AlienBullet(ai_settings, screen, alien)
        alienBullets.add(new_alienbullet)

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, alienBullets, bosses):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        #将ships_left减1
        stats.ships_left -= 1

        #更新记分牌
        sb.prep_ships()
    
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        alienBullets.empty()
        bosses.empty()

        stats.aims = 10 + 5*stats.level
        stats.kill_boss = 2*stats.level
    
        #创建新的外星人，并将飞船放到屏幕底端中央
        create_alien(ai_settings, screen, aliens)
        #create_alienbullets(ai_settings, screen, aliens, alienBullets)
        ship.center_ship()
    
        #暂停
        sleep(2)
        
    else:
        stats.game_active = False
        aliens.empty()
        bullets.empty()
        bosses.empty()
        alienBullets.empty()
        pygame.mouse.set_visible(True)
    
def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets, alienBullets, bosses):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #将消失的外星人删除
            aliens.remove(alien)
    for boss in bosses.sprites():
        if boss.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets,alienBullets, bosses)
            break

def check_boss_side(screen,bosses, aliens):
    """检查boss是否到达了屏幕边缘"""
    screen_rect = screen.get_rect()
    for boss in bosses.sprites():
        if boss.rect.left <= 0 or boss.rect.right >= screen_rect.right or pygame.sprite.groupcollide(bosses, aliens, False, False):
            boss.speed_factor_direction *= -1

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets, alienBullets, bosses):
    """检查是否有外星人位于屏幕边缘，并更新外星人群中所有外星人的位置"""
    #check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #检测屏幕上同时存在的外星人是否超过了限制
    if len(aliens) < ai_settings.alien_limit:
        create_alien(ai_settings, screen, aliens)
        create_alienbullets(ai_settings, screen, aliens, alienBullets)
    
    #检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens) or pygame.sprite.spritecollideany(ship, alienBullets) or pygame.sprite.spritecollideany(ship, bosses):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets,alienBullets, bosses)
        
    #检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets, alienBullets, bosses)

    #检查boss是否到达了屏幕边缘
    check_boss_side(screen, bosses, aliens)
    bosses.update()