import pygame
from bullet import *
# pygame.mixer.init()
# 飞机


class HeroPlane(object):
    # 飞机初始化
    def __init__(self, scene):
        # 加载飞机资源
        self.image = pygame.image.load("./images/hero/hero.png")
        self.mask = pygame.mask.from_surface(self.image)
        # 缓存主场景对象
        self.main_scene = scene
        # 飞机矩形
        self.rect = self.image.get_rect()
        # 矩形起始点
        self.rect[0] = self.main_scene.size[0] / 2 - self.rect[2] / 2
        self.rect[1] = self.main_scene.size[1] - self.rect[3] * 2
        # 飞机子弹列表
        self.bullets = [Bullet(self.main_scene) for _ in range(0, 30)]

        self.endtime = pygame.time.get_ticks()
        self.interval = 200
        # 储存键盘的'a s d w'键，控制飞机移动
        self.key_down_list = []
        self.space_key_list = []
        self.speed = 4
        self.HP = 10
        self.invincible = False

    # def rect(self):
    #     return self.rect

    # 发子弹

    def shot(self):
        # mixer.Sound 貌似无法识别 mp3格式
        mus = pygame.mixer.Sound('musics/hero_fire.wav')
        mus.set_volume(4)
        mus.play()

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
        posx = self.rect[0] - 9
        # # 依次设置选择子弹的初始位置，并将其设置为发射状态、移动速度
        for bullet in wait_for_shot:
            bullet.visible = True
            bullet.set_speed(4)
            bullet.set_pos(posx, self.rect[1] - self.rect[3] / 2)
            posx = posx + self.rect[2]/2

        # self.main_clock.tick(40)

    def move(self, direction):
        if direction == "RIGHT":
            self.rect[0] = self.rect[0] + self.speed
        elif direction == "LEFT":
            self.rect[0] = self.rect[0] - self.speed
        elif direction == "UP":
            self.rect[1] = self.rect[1] - self.speed
        elif direction == 'DOWN':
            self.rect[1] = self.rect[1] + self.speed

    def move_limit(self):
        if self.rect[0] < -30:
            self.rect[0] = -30
        elif self.rect[0] > self.main_scene.size[0]-30:
            self.rect[0] = self.main_scene.size[0]-30

    # 飞机动作
    def action(self, x, y):
        self.rect[0] = x - self.rect[2] / 2
        self.rect[1] = y - self.rect[3] / 2

    # 飞机绘制
    def draw(self):
        self.move_limit()
        for bullet in self.bullets:
            if bullet.visible:
                bullet.draw()
        self.main_scene.scene.blit(self.image, (self.rect[0], self.rect[1]))

    # 储存按键到列表
    def key_down(self, key):
        self.key_down_list.append(key)

    def key_up(self, key):
        if len(self.key_down_list) != 0:
            try:
                self.key_down_list.remove(key)
            except Exception:
                pass

    def press_move(self):
        if len(self.key_down_list) != 0:
            if self.key_down_list[0] == pygame.K_a:
                self.move('LEFT')
            elif self.key_down_list[0] == pygame.K_d:
                self.move('RIGHT')
            elif self.key_down_list[0] == pygame.K_w:
                self.move('UP')
            elif self.key_down_list[0] == pygame.K_s:
                self.move("DOWN")

    # 键盘按下向列表添加space
    def space_key_down(self, key):
        self.space_key_list.append(key)

    # 键盘松开向列表删除space
    def space_key_up(self, key):
        if len(self.space_key_list) != 0:  # 判断是否为空
            try:
                self.space_key_list.remove(key)
            except Exception:
                raise
    # 按键space不放,持续开火

    def press_fire(self):
        starttime = pygame.time.get_ticks()
        passtime = starttime - self.endtime

        if len(self.space_key_list) != 0 and passtime > self.interval:
            # and passtime >100:
            self.shot()
            self.endtime = starttime
