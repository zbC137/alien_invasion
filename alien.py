# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 14:50:46 2019

@author: zbin13
"""

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """表示单个外星人的类"""
    
    def __init__(self, ai_settings, screen):
        """初始化外星人并设置其起始位置"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        #加载外星人图像，并设置其rect属性
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        
        #每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #存储外星人的准确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.speed_factor = self.ai_settings.alien_speed_factor
        
    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)
    
    def update(self):
        """向下移动外星人"""
        self.y += self.speed_factor
        self.rect.y = self.y