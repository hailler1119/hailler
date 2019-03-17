import pygame

# 地图


class GameBackground(object):
    # 初始化地图
    def __init__(self, scene):
        # 加载相同张图片资源,做交替实现地图滚动
        self.image1 = pygame.image.load("images/bg1.jpg")
        self.image2 = pygame.image.load("images/bg1.jpg")
        # 保存场景对象
        self.main_scene = scene
        # 辅助移动地图
        self.image1_rect = self.image1.get_rect()
        self.image2_rect = self.image2.get_rect()
        self.y1 = self.main_scene.size[1] - self.image1_rect.height
        self.y2 = self.y1 - self.image2_rect.height

    # 计算地图图片绘制坐标
    def action(self):
        self.y1 = self.y1 + 1
        self.y2 = self.y2 + 1
        if self.y1 >= self.main_scene.size[1]:
            self.y1 = self.y2 - self.image1_rect.height
        if self.y2 >= self.main_scene.size[1]:
            self.y2 = self.y1 - self.image2_rect.height

    # 绘制地图的两张图片
    def draw(self):
        self.main_scene.scene.blit(self.image1, (0, self.y1))
        self.main_scene.scene.blit(self.image2, (0, self.y2))
