import pygame
import random
from pygame.locals import *
from random import randrange
from airplane import Airplane
from bullet import Bullet
import virusers


def loadgameover(scorenum):  # 绘出GAME OVER
    screen.fill([0, 0, 0])
    my_font = pygame.font.SysFont('arial', 50)
    levelstr = 'GAME OVER'  #游戏结束
    over_screen = my_font.render(levelstr, True, (255, 0, 0))
    screen.blit(over_screen, (200, 240))
    highscorestr = 'YOUR SCORE IS ' + str(scorenum)  #显示得分
    over_screen = my_font.render(highscorestr, True, (255, 0, 0))
    screen.blit(over_screen, (200, 290))
    global count_num   #分数是一个全局变量，在这里重置为0
    count_num = 0
    airplane.rect.centerx = 300  #飞机位置重置
    airplane.rect.top = 800 - 54
    pygame.display.update()  # 刷新
    pygame.time.delay(1000)


if __name__ == '__main__':
    pygame.init()  # 初始化
    pygame.mixer.init()

    virusers.viruse_new()  # 病毒实例化
    #窗口初始化
    screen = pygame.display.set_mode((600,800))
    pygame.display.set_caption('消灭病毒')
    window_image = pygame.image.load('./airplane.jpg')
    pygame.display.set_icon(window_image)
    # 帧率设置
    clock = pygame.time.Clock()
    # 左上角计算分数
    countObj = pygame.font.SysFont('arial', 50)
    textObj = countObj.render('SCORE:0', True, (255, 0, 0))
    textRectObj = textObj.get_rect()
    screen.blit(textObj, textRectObj)
    # 这个是计算分数
    count_num = 0
    # 创建飞机
    airplane = Airplane(screen)
    # 子弹容器
    bullet_sprites = pygame.sprite.RenderUpdates()  # 创建sprite容器  树
    AddEnemy = pygame.USEREVENT + 1  # 添加子弹的时间
    pygame.time.set_timer(AddEnemy, 300)

    pygame.display.flip()
    while True:
        clock.tick(60)
        screen.fill((255, 255, 255))  # 背景色
        screen.blit(airplane.image, airplane.rect)
        ''' 添加新病毒 '''
        if virusers.group.__len__() < 3:
            virusers.viruse_new()  # 病毒实例化

        virusers.group.update()  # 病毒
        virusers.group.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == AddEnemy:
                bullet_sprites.add(Bullet(screen, airplane))
            elif event.type == pygame.K_BACKSPACE:
                loadgameover(count_num)

        # 获取键盘状态
        pressed_keys = pygame.key.get_pressed()
        # 调用方法更新
        airplane.update(pressed_keys)
        # 场景动画更新
        bullet_sprites.update()
        bullet_updates = bullet_sprites.draw(screen)
        pygame.display.update(bullet_updates)

        # 子弹和病毒组的碰撞
        hit_list = pygame.sprite.groupcollide(bullet_sprites, virusers.group, True, False)
        '''得分'''
        if hit_list.values().__len__():  # hit_list.values() 返回就是病毒精灵
            for obj in hit_list.values():
                if obj[0].score > 10:
                    obj[0].score -= 10
                else:
                    obj[0].kill()
                count_num += 10
        '''结束游戏 '''
        game_over = pygame.sprite.spritecollide(airplane, virusers.group, False)
        if game_over:
            if not game_over[0].Flag:
                loadgameover(count_num)
                # game_over[0].kill()
                game_over[0].Flag = True

        # 得分多少
        textObj = countObj.render('SCORE:%d' % count_num, False, (255, 0, 0))  # 显示得分内容
        textRectObj = textObj.get_rect()
        screen.blit(textObj, textRectObj)  # 这是得分
        pygame.display.flip()
        pygame.display.update()  # 刷新
