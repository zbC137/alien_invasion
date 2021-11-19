# -*- coding: utf-8 -*-
#============================
# Author: Bran Zhang
# Date: Aug.19th, 2019
#============================

import pygame

class Music_Button_Ingame():
    
    def __init__(self, ai_settings, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        #设置按钮的尺寸和其他属性
        self.width, self.height = 50, 25
        self.button_color = (178, 215, 240)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('arial', 20)

        #创建按钮的rect对象
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx - 50
        self.rect.top = 8
        
        #按钮的标签只需创建一次
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """将msg渲染为图像，并使其在按钮上居中"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #绘制一个用颜色填充的按钮，再绘制文本
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)