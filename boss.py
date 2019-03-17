import pygame
from enemyplane import *


class BossPlane(EnemyPlane):
    def __init__(self, scene):
        # 加载飞机资源
        self.images = [pygame.image.load(
            "./images/boss/" + str(v) + ".png") for v in range(0, 11)]
        self.image = self.images[0]
        self.mask = pygame.mask.from_surface(self.image)
        # 缓存主场景对象
        self.main_scene = scene
       # 设置当前BOSS图片播放索引
        self.index = 0
        # 图片BOSS图片播放间隔
        self.interval = 20
        self.interval_index = 0
        # 飞机矩形
        self.rect = pygame.image.load('images/boss/0.png').get_rect()
        self.size = self.rect.bottomright

        # 子弹列表
        self.bullets = [Bullet(self.main_scene, enemy=True, type=0)
                        for v in range(0, 21)]
        # 飞机速度
        self.speed = 3
        # 飞机血量
        self.HP = 1000
        self.score = 100
        # BOSS 是否可见
        self.visible = False
        # 飞机子弹发射间隔 毫秒

        self.interval = 1500
        # 飞机子弹发射当前时间
        self.endtime = pygame.time.get_ticks()

       # 飞机动作
    def action(self):
        # 左右移动
        leftX = - self.size[0]/2
        rightX = self.main_scene.size[0] - self.size[0]/2

        if self.rect[0] < leftX or self.rect[0] > rightX:
            self.speed = -self.speed
        self.rect[0] += self.speed
        # 如果飞机移动出屏幕则将飞机设置为初始
        if self.rect[1] > self.main_scene.size[1]:
            self.set_pos(240, 0)

        self.interval_index += 1
        if self.interval_index < self.interval:
            return
        self.interval_index = 0

        self.index = self.index + 1
        if self.index >= len(self.images):
            self.index = 0
            self.visible = False
        self.image = self.images[self.index]
        self.mask = pygame.mask.from_surface(self.image)

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
        posx = self.rect[0] - 15
        # 依次设置选择子弹的初始位置，并将其设置为发射状态、移动速度
        for bullet in wait_for_shot:
            bullet.visible = True
            posx = posx + 30
            bullet.set_speed(4)
            bullet.set_pos(posx + 3, self.rect[1] + self.rect[3] / 2)

    def draw(self):
        for bullet in self.bullets:
            if bullet.visible:
                bullet.draw()
        # if not self.visible:
        #     return
        self.main_scene.scene.blit(
            self.images[self.index], (self.rect[0], self.rect[1]))
        # print('BOSS HP' + str(self.HP))
