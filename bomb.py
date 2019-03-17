import pygame


class Bomb(object):
    # 初始化爆炸
    def __init__(self, scene):
        self.main_scene = scene
        # 加载爆炸资源,两种方法。
        # 方法一 加载单张图片的列表
        # self.images = [pygame.image.load("images/bomb/bomb" + str(v) + ".png") for v in range(1, 3)]
        # 方法二 单张图片切片,真是信了你的邪了，load error.要绝对路径才能运行。更邪的是后来相对路径也可以了。
       # 爆炸特效的帧列表
        self.images = []
        # self.boom_picture = pygame.image.load("E:/自学飞机大战/day7/images/bomb/bomb.png")
        self.boom_picture = pygame.image.load(
            "./images/bomb/bomb.png").convert_alpha()
        for r in range(4):
            for c in range(8):
                frame = self.boom_picture.subsurface(
                    [c * 82 + 2 * (4 - r), r * 82, 75, 82])
                self.images.append(frame)
        # 设置当前爆炸播放索引
        self.index = 0
        # 图片爆炸播放间隔
        self.interval = 2
        self.interval_index = 0
        # 爆炸位置
        self.position = [0, 0]
        # 是否可见
        self.visible = False

    # 设置爆炸播放的位置
    def set_pos(self, x, y):
        self.position[0] = x - 25
        self.position[1] = y

    # 爆炸播放
    def action(self):
        # 如果爆炸对象状态不可见，则不计算坐标
        if not self.visible:
            return

        # 控制每一帧图片的播放间隔
        self.interval_index += 1
        if self.interval_index < self.interval:
            return
        self.interval_index = 0

        self.index = self.index + 1
        if self.index >= len(self.images):
            self.index = 0
            self.visible = False

    # 绘制爆炸
    def draw(self):
        # 如果对象不可见，则不绘制
        if not self.visible:
            return
        self.main_scene.scene.blit(
            self.images[self.index], (self.position[0], self.position[1]))
