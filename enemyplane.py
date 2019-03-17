import pygame
import random

from bullet import *

# 敌人飞机


class EnemyPlane(object):
    # 初始化敌人飞机
    def __init__(self, scene, type=1):
         # 加载飞机资源
            # 缓存主场景对象
        self.main_scene = scene
        self.type = type
        self.HP = 1
        self.score = 1
        self.visible = True
        if self.type == 1:
            self.image = pygame.image.load("./images/enemy/enemy1.png")
            # 飞机矩形
            self.rect = self.image.get_rect()
            # 子弹列表
            self.bullets = [Bullet(self.main_scene, enemy=True)
                            for v in range(1, 9)]
            # 飞机速度
            self.speed = 2
            self.score = 1
            # 子弹间隔
            self.interval = 1000
        elif self.type == 2:
            self.image = pygame.image.load("./images/enemy/enemy2.png")
            # 飞机矩形
            self.rect = self.image.get_rect()
            # 子弹列表
            self.bullets = [Bullet(self.main_scene, enemy=True, type=2)
                            for v in range(1, 12)]
            # self.bullet = Bullet(self.main_scene, True)
            # 飞机速度
            self.speed = 3
            self.score = 2
            self.interval = 2000
        elif self.type == 3:
            self.image = pygame.image.load("./images/enemy/enemy3.png")

            # 飞机矩形
            self.rect = self.image.get_rect()
            # 子弹列表
            self.bullets = [Bullet(self.main_scene, enemy=True, type=3)
                            for v in range(1, 12)]
            # 飞机速度
            self.speed = 3
            self.score = 3
            self.HP = 10
            self.interval = 1500
        elif self.type == 4:
            self.image = pygame.image.load("./images/enemy/enemy4.png")

            # 飞机矩形
            self.rect = self.image.get_rect()
            # 子弹列表
            self.bullets = [Bullet(self.main_scene, enemy=True, type=4)
                            for v in range(1, 12)]
            # 飞机速度
            self.speed = 3
            self.score = 4
            self.HP = 12
            self.interval = 1500
        elif self.type == 5:
            self.image = pygame.image.load("./images/enemy/enemy5.png")

            # 飞机矩形
            self.rect = self.image.get_rect()
            # 子弹列表
            self.bullets = [Bullet(self.main_scene, enemy=True, type=5)
                            for v in range(1, 12)]
            # 飞机速度
            self.speed = 3
            self.score = 5
            self.HP = 15
            self.interval = 1500
        elif self.type == 6:
            self.image = pygame.image.load("./images/enemy/enemy6.png")

            # 飞机矩形
            self.rect = self.image.get_rect()
            # 子弹列表
            self.bullets = [Bullet(self.main_scene, enemy=True, type=5)
                            for v in range(1, 12)]
            # 飞机速度
            self.speed = 3
            self.score = 5
            self.HP = 15
            self.interval = 1500

        # 默认
        else:
            self.image = pygame.image.load("./images/enemy/enemy1.png")
            # 飞机矩形
            self.rect = self.image.get_rect()
            # 子弹列表
            self.bullets = [Bullet(self.main_scene, enemy=True)
                            for v in range(1, 9)]
            # 飞机速度
            self.speed = 2
            # 飞机生命
            self.HP = 10
            # 子弹间隔
            self.interval = 1000

        self.endtime = pygame.time.get_ticks()
        self.set_pos(random.randint(
            0, self.main_scene.size[1] - self.rect[2] - 20), 0)
    # 获得飞机矩形

    def rect(self):
        return self.rect

    # 设置飞机位置
    def set_pos(self, x, y):
        self.rect[0] = x
        self.rect[1] = y

    def shot(self):
        starttime = pygame.time.get_ticks()
        passtime = starttime - self.endtime
        if passtime < self.interval:
            return
        self.endtime = starttime

        # 每次发射三颗子弹
        wait_for_shot = []
        # 从子弹列表取出3颗目前尚未发射的子弹
        # 如果子弹的visible为false，说明子弹尚未发射
        for bullet in self.bullets:
            # 如果子弹不可见,说明子弹闲置状态
            if not bullet.visible:
                wait_for_shot.append(bullet)
                if len(wait_for_shot) >= 3:
                    break
        # 子弹发射位置，从posx位置开始 向右排列三颗子弹
        # 子弹发射位置，从posx位置开始 向右排列三颗子弹
        posx = self.rect[0] - 9
        # # 依次设置选择子弹的初始位置，并将其设置为发射状态、移动速度
        for bullet in wait_for_shot:
            bullet.visible = True
            bullet.set_speed(5)
            bullet.set_pos(posx, self.rect[1] + self.rect[3] / 2)
            posx = posx + self.rect[2]/2

    # 飞机动作
    def action(self):
        # 飞机每次移动向上移动self.speed速度
        self.rect.move_ip(0, self.speed)
        # 如果飞机移动出屏幕则将飞机设置为不可见状态
        if self.rect[1] > self.main_scene.size[1]:
            self.visible = False

    # 绘制飞机 和发出的子弹。子弹在哪里实现，都很别扭。在这里实现，就不能用remove了。
    def draw(self):
        for bullet in self.bullets:
            if bullet.visible:
                bullet.draw()
        if not self.visible:
            return
        self.main_scene.scene.blit(self.image, (self.rect[0], self.rect[1]))
