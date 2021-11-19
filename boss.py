# -*- coding:utf-8 -*-
#========================
#Author: Bin Zhang
#Date: Sep. 16th, 2019
#========================


import pygame
from pygame.sprite import Sprite

class Boss(Sprite):
    """表示通关boss的类"""
    
    def __init__(self, ai_settings, screen):
        """初始化boss并设置其起始位置"""
        super(Boss, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        #加载外星人图像，并设置其rect属性
        self.image = pygame.image.load('images/boss.bmp')
        self.rect = self.image.get_rect()
        
        #每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #存储外星人的准确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.speed_factor = self.ai_settings.boss_speed_factor
        self.speed_factor_direction = 1
        
    def blitme(self):
        """在指定位置绘制boss"""
        self.screen.blit(self.image, self.rect)
    
    def update(self):
        """移动boss"""
        self.y += self.speed_factor
        self.rect.y = self.y
        self.x += self.speed_factor*self.speed_factor_direction
        self.rect.x = self.x