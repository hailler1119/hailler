import pygame
# 子弹


class Bullet(object):
    # 初始化子弹
    def __init__(self, scene, enemy=False, type=1):
        # 子弹移动速度
        self.speed = 2
        # 是否是敌人子弹
        self.is_enemy = enemy
        # self.is_boss = boss
        self.type = type
        self.image = pygame.image.load("./images/bullet/enemybullet1.png")
        # 子弹资源
        if self.is_enemy:
            if self.type == 1:
                # 加载敌人子弹图片
                self.image = pygame.image.load(
                    "./images/bullet/enemybullet1.png")
                # 设置子弹移动方向
                self.speed = self.speed
            elif self.type == 2:
                 # 加载敌人子弹图片
                self.image = pygame.image.load(
                    "./images/bullet/enemybullet2.png")
                # 设置子弹移动方向
                self.speed = self.speed + 2
            elif self.type == 3:
                 # 加载敌人子弹图片
                self.image = pygame.image.load(
                    "./images/bullet/enemybullet3.png")
                # 设置子弹移动方向
                self.speed = self.speed + 4
            elif self.type == 0:  # BOSS
                self.image = pygame.image.load(
                    "./images/bullet/bossbullet.png")
                self.speed = 4
            else:
                 # 加载敌人子弹默认图片
                self.image = pygame.image.load(
                    "./images/bullet/enemybullet1.png")
                # 设置子弹移动方向
                self.speed = self.speed
        else:
            # 加载英雄子弹图片
            self.image = pygame.image.load("./images/bullet/herobullet.png")
            # 设置子弹移动方向
            self.speed = -self.speed

        self.visible = False
        # 持有主场景对象
        self.main_scene = scene
        # 获得子弹矩形(x, y, width, height)
        self.rect = self.image.get_rect()

    # 设置子弹位置
    def set_pos(self, x, y):
        self.rect[0] = x
        self.rect[1] = y

    # 设置子弹速度
    def set_speed(self, speed):
        if self.is_enemy:
            self.speed = speed
        else:
            self.speed = -speed

    # 子弹移动

    def action(self):
        if not self.visible:
            return
        # 假设飞机矩形为plane_rect(10, 20, 200, 300)
        # plane_rect.move_ip(10, 20), 那么结果是plane_rect(20, 40, 200, 300)
        # 也就是原矩形x和y坐标加上move_ip函数x和y坐标，就是当前矩形新位置
        self.rect.move_ip(0, self.speed)
        # 如果子弹超出场景范围,则设置为不可见
        if self.rect[1] < 0 or self.rect[1] > self.main_scene.size[1]:
            self.visible = False

    # 绘制子弹
    def draw(self):
        if not self.visible:
            return
        self.main_scene.scene.blit(self.image, (self.rect[0], self.rect[1]))
