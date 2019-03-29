#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pygame
import sys
import random


# 病毒类
class Viruses(pygame.sprite.Sprite):
    Flag = False

    def __init__(self, image, position, x_speed, y_speed):
        '''
        初始化
        :param image: 图片名字
        :param position: 位置
        :param x_speed: 水平的速度
        :param y_speed: 竖直的速度
        :param score:  生命值
        '''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.X_speed = x_speed
        self.Y_speed = y_speed
        if image == '2.png':
            self.score = 20
        elif image == '3.png':
            self.score = 10

    ''' 移动 '''
    def update(self, *args):
        self.rect = self.rect.move(self.X_speed, self.Y_speed)
        if self.rect.left < 0 or self.rect.right > 600:
            self.X_speed = -self.X_speed
        if self.rect.bottom > 800 + self.rect.height:
            self.rect.top = -self.rect.height
        if self.score == 0:
            self.kill()
        elif self.score == 10:
            self.trun(1)



    ''' 换图 '''
    def trun(self, value):
        if value == 0:
            self.image = pygame.image.load(viruses_images[value])
        elif value == 1:
            self.image = pygame.image.load(viruses_images[value])


group = pygame.sprite.Group()
viruses_images = ['2.png', '3.png']


# 初始化精灵组
def viruse_new():
    position_list = []
    for i in range(10):
        row = random.randint(0, 9)
        col = random.randint(0, 9)
        position = [row * 60 + 21, - col * 60 - 30]
        if position not in position_list:
            position_list.append(position)
            image_name = random.choice(viruses_images)
            obj = Viruses(image_name, position, random.randint(1, 3), random.randint(1, 3))
            group.add(obj)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((600, 800))
    pygame.display.set_caption('嘿嘿嘿')

    viruses_images = ['2.png', '3.png']

    clock = pygame.time.Clock()  # 设置帧率, 也可以理解为延时

    group = pygame.sprite.Group()  # 设置精灵组
    viruse_new()

    while True:
        clock.tick(100)
        '''关闭窗口'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 关闭窗口
                sys.exit()

        group.update()
        screen.fill([255, 255, 255])

        group.draw(screen)
        pygame.display.update()  # 刷新
