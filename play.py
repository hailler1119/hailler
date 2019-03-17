import pygame
import random
from sys import exit
from pygame.locals import *
from gamebackground import *
from heroplane import *
from enemyplane import *
from bomb import *
from boss import *
from gameinfo import *


# 主场景
class MainScene(object):
    # 初始化主场景
    def __init__(self):
        pygame.mixer.pre_init()
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        # 场景尺寸
        self.size = (600, 800)
        # 场景对象
        self.scene = pygame.display.set_mode(
            [self.size[0], self.size[1]], 1, 32)
        # 设置标题
        pygame.display.set_caption("飞机大战-v1.0")
        # 地图对象
        self.map = GameBackground(self)
        # 英雄对象
        self.hero = HeroPlane(self)
        # 创建多个敌机
        self.enemy_list = [EnemyPlane(self) for v in range(5)]

        # 创建BOSS
        self.boss_list = []
        # self.boss_list = [BossPlane(self) for v in range(1)]
        # 创建爆炸对象
        self.bombs = [Bomb(self) for v in range(15)]
        self.my_font = pygame.font.SysFont('kaiti', 16, True, True)
        self.score_font = pygame.font.SysFont('kaiti', 30, True, True)

        # 创建记录
        self.hero_score = 0
        # 游戏等级
        self.gamelevel = 1
        # 无敌时间两秒,不然撞了飞机直接完蛋
        self.invincible_start = pygame.time.get_ticks()
        self.gameover = False
        # 自定义事件
        self.ADDENEMY6 = pygame.USEREVENT + 1
        # 事件本质上就是整数常量。比 USEREVENT 小的数值已经对应内置事件，因此任何自定义事件都要比 USEREVENT 大
        self.ADDENEMY1 = pygame.USEREVENT + 2
        pygame.time.set_timer(self.ADDENEMY6, 8000)  # 每隔 8000ms 触发
        pygame.time.set_timer(self.ADDENEMY1, 5000)

    # 绘制
    def draw_elements(self):
        if self.gameover:
            return
        # 绘制地图
        self.map.draw()
        # 绘制英雄飞机
        self.hero.draw()
        # 依次绘制英雄飞机每一颗发射出去的子弹
        # 英雄子弹的绘制在他自己的函数里了。
        # 绘制敌人飞机和飞机子弹
        for enemy in self.enemy_list:
            # 如果敌人已经死亡或者逃掉，清理出列表。不然会卡卡的要死的。但enemy删除后，他的子项
            # 也跟着删除了，bullet瞬间消失， 子弹在飞就难了，难道子弹也要子弹精灵？。
            # 找到解决办法了，把子弹也存到当前class里面，self.enemy_bullet_list][],
            # 在子弹的bullet.py里添加一个属性, 列如 self.outscene 子弹跑到屏幕外就设置成True,
            # 在这里判断，if bullet.outscent == True: enemy_bullet_liset.remove(bullet)
            # 这样跑出屏幕的子弹也自动删除，而敌机被击落后，打出的子弹在屏幕内不会删除，还能继续运动。
            # 需要在draw() 和 action ()里面都添加子弹绘制和动作函数。
            if not enemy.visible:
                self.enemy_list.remove(enemy)
            else:
                enemy.draw()
        # 绘制BOSS机
        for boss in self.boss_list:
            # boss_life = self.my_font.render('BOSS life:' + str(boss.HP),True,(0,0,255))
            # self.scene.blit(boss_life,(self.size[0]/2-200,0))
            hp_remain = boss.HP/1000
            if hp_remain < 0:
                hp_remain = 0
            # red  = (255,0,0)
            # greed = (0,255,0)
            if hp_remain > 0.25:
                pygame.draw.line(self.scene, (0, 255, 0),
                                 (200, 0), (200+300*hp_remain, 0), 30)
            else:
                pygame.draw.line(self.scene, (255, 0, 0),
                                 (200, 0), (200+300*hp_remain, 0), 30)
            if boss.visible:
                boss.draw()
        # 绘制爆炸图片
        for bomb in self.bombs:
            if bomb.visible:
                bomb.draw()
        # 绘制玩家信息
        hero_info = self.my_font.render(
            'score:' + str(self.hero_score), True, (255, 0, 0))
        hero_life = self.my_font.render(
            "生命:" + str(self.hero.HP), True, (0, 255, 0))

        self.scene.blit(hero_info, (0, 0))
        self.scene.blit(hero_life, (self.size[0] - 100, 0))

    # 动作
    def action_elements(self):
            # 计算坐标地图
        self.map.action()
        # 依次计算英雄飞机每一颗发射子弹的坐标
        for bullet in self.hero.bullets:
            if bullet.visible:
                bullet.action()
        # 计算敌人飞机和其飞机子弹
        for plane in self.enemy_list:
            plane.action()
            plane.shot()
            for bullet in plane.bullets:
                if bullet.visible:
                    bullet.action()
        for boss in self.boss_list:

            boss.action()
            boss.shot()
            for bullet in boss.bullets:
                if bullet.visible:
                    bullet.action()
        # 切换爆炸图片
        for bomb in self.bombs:
            if bomb.visible:
                bomb.action()

    # 处理事件
    def handle_event(self):

        event_list = pygame.event.get()
        # 遍历事件列表
        for event in event_list:
            # 如果判断用户点击了X按钮，则结束程序
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # 判断事件类型是否是键盘按下事件
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    #  self.hero.shot()
                    self.hero.space_key_down(pygame.K_j)
                elif event.key == pygame.K_a:
                    self.hero.key_down(pygame.K_a)
                elif event.key == pygame.K_d:
                    self.hero.key_down(pygame.K_d)
                elif event.key == pygame.K_w:
                    self.hero.key_down(pygame.K_w)
                elif event.key == pygame.K_s:
                    self.hero.key_down(pygame.K_s)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.hero.key_up(pygame.K_a)
                elif event.key == pygame.K_d:
                    self.hero.key_up(pygame.K_d)
                elif event.key == pygame.K_w:
                    self.hero.key_up(pygame.K_w)
                elif event.key == pygame.K_s:
                    self.hero.key_up(pygame.K_s)
                elif event.key == pygame.K_j:
                    self.hero.space_key_up(pygame.K_j)
            elif event.type == self.ADDENEMY6:
                self.enemy_list.append(EnemyPlane(self, type=6))
            elif event.type == self.ADDENEMY1:
                self.enemy_list.append(EnemyPlane(self, type=5))
                # self.enemy_list.append(EnemyPlane(self,type = 3 ))
            # 判断是否发生了鼠标拖动事件
            if event.type == pygame.MOUSEMOTION:
                # 获得鼠标点击三个按钮的点击情况(1,0,0)
                # 如果第一个参数为1,表示左键被按下
                # 如果第二个参数为1,表示滚轮被按下
                # 如果第三个参数为1,表示右键被按下
                buttons = pygame.mouse.get_pressed()
                # 我们只处理左键被按下的情况
                if buttons[0]:
                    # 获得拖动鼠标的拖动位置
                    position = pygame.mouse.get_pos()
                    # 飞机跟随坐标移动
                    # print(position)
                    self.hero.action(position[0], position[1])

        self.hero.press_move()
        self.hero.press_fire()

    # 碰撞检测

    def detect_conlision(self):
        # 英雄机和飞机碰撞检查包括BOSS机
        enemyscrash = pygame.sprite.spritecollide(self.hero, self.enemy_list, False, pygame.sprite.collide_mask)\
            or pygame.sprite.spritecollide(self.hero, self.boss_list, False)
        if enemyscrash:
            self.hero_score += 1
            for enemy in enemyscrash:
                current_time = pygame.time.get_ticks()
                if current_time - self.invincible_start < 2000:
                    return
                self.invincible_start = current_time
                self.hero.HP -= 1
                for bomb in self.bombs:
                    if not bomb.visible:
                        # 爆炸对象设置爆炸位置
                        bomb.set_pos(self.hero.rect[0], self.hero.rect[1])
                        # 爆炸对象状态设置为True
                        bomb.visible = True

        # 英雄机和敌人子弹碰撞检查
        for enemy in self.enemy_list:
            # 找到所有击中英雄飞机的子弹
            enemybullets = pygame.sprite.spritecollide(
                self.hero, enemy.bullets, False, pygame.sprite.collide_mask)
            if enemybullets:
                for bullet in enemybullets:
                    if not bullet.visible:
                        continue
                    bullet.visible = False
                    self.hero.HP -= 1
                    # 从预先创建完毕的爆炸中取出一个爆炸对象
                    for bomb in self.bombs:
                        if not bomb.visible:
                            # 爆炸对象设置爆炸位置
                            bomb.set_pos(self.hero.rect[0], self.hero.rect[1])
                            # 爆炸对象状态设置为True
                            bomb.visible = True
        # 英雄机和BOSS子弹碰撞检查
        for boss in self.boss_list:
            # 找到所有击中英雄飞机的子弹
            bossbullets = pygame.sprite.spritecollide(
                self.hero, boss.bullets, False, pygame.sprite.collide_mask)
            if bossbullets:
                for bullet in bossbullets:
                    if not bullet.visible:
                        continue
                    bullet.visible = False
                    self.hero.HP -= 1
                    # 从预先创建完毕的爆炸中取出一个爆炸对象
                    for bomb in self.bombs:
                        if not bomb.visible:
                            # 爆炸对象设置爆炸位置
                            bomb.set_pos(self.hero.rect[0], self.hero.rect[1])
                            # 爆炸对象状态设置为True
                            bomb.visible = True

        # # 检测英雄子弹是否和敌机碰撞
        for enemy in self.enemy_list:
            # 击中敌人飞机的英雄飞机子弹
            herobullets = pygame.sprite.spritecollide(
                enemy, self.hero.bullets, False, pygame.sprite.collide_mask)
            if herobullets:
                for bullet in herobullets:
                    if not bullet.visible:
                        continue
                    bullet.visible = False
                    for bomb in self.bombs:
                        if not bomb.visible:
                            bomb.set_pos(enemy.rect[0], enemy.rect[1])
                            bomb.visible = True
                            mus = pygame.mixer.Sound('./musics/boom_music.ogg')
                            mus.set_volume(6)
                            mus.play()
                    enemy.visible = False
                    self.hero_score += enemy.score

        # 英雄机子弹是否和boss相撞
        for boss in self.boss_list:
            if not boss.visible:
                continue
            # 击中BOSS飞机的英雄飞机子弹
            herobullets = pygame.sprite.spritecollide(
                boss, self.hero.bullets, False, pygame.sprite.collide_mask)
            if herobullets:
                for bullet in herobullets:
                    if not bullet.visible:
                        continue
                    bullet.visible = False
                    boss.HP -= 10
                    if boss.HP >= 0:
                        continue
                    for bomb in self.bombs:
                        if not bomb.visible:
                            bomb.set_pos(boss.rect[0], boss.rect[1])
                            bomb.visible = True

                            mus = pygame.mixer.Sound('./musics/boom_music.ogg')
                            mus.set_volume(6)
                            mus.play()
                            # 添加 boss 移除代码
                            self.boss_list[0].visible = False
                            # self.boss_list[boss.index].visible = False
                            self.hero_score += boss.score

        # 检查完毕，英雄是否没有血量了
        if self.hero.HP <= 0:
            self.gameover = True

    def change_level(self):
        if self.gamelevel == 1 and self.hero_score > LEVEL1_SCORE:
            self.enemy_list.append(EnemyPlane(self, type=2))
            self.enemy_list.append(EnemyPlane(self, type=3))
            self.gamelevel = 2
        elif self.gamelevel == 2 and self.hero_score > LEVEL2_SCORE:
            for v in range(1, 3):
                self.enemy_list.append(EnemyPlane(self, type=4))
                # self.enemy_list.append(EnemyPlane(self, type = 5))
            self.gamelevel = 3
        elif self.gamelevel == 3 and self.hero_score > LEVEL3_SCORE:
            self.boss_list = [BossPlane(self)]
            # 续添加list[x]判断
            self.boss_list[0].visible = True
            self.gamelevel = 4
        else:
            pass

    def game_over(self):
        if self.hero.HP >= 0:
            return
        # print('gameover')
        pygame.mixer.music.stop()
        pygame.mixer.stop()
        hero_info = self.my_font.render(
            'score:' + str(self.hero_score), True, (255, 0, 0))
        hero_life = self.my_font.render("生命: 0", True, (0, 255, 0))
        self.scene.blit(hero_info, (0, 0))
        self.scene.blit(hero_life, (self.size[0] - 100, 0))

        game_restart_image = pygame.image.load('./images/menu/restart.png')
        game_restart_rect = game_restart_image.get_rect()
        game_restart_rect.left, game_restart_rect.top = self.size[0] / \
            2 - 100, self.size[1]/2 - 200

        game_over_image = pygame.image.load('./images/menu/quit.png')
        game_over_rect = game_over_image.get_rect()
        game_over_rect.left, game_over_rect.top = self.size[0] / \
            2 - 100, self.size[1]/2
        self.scene.blit(game_restart_image, game_restart_rect)
        self.scene.blit(game_over_image, game_over_rect)
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            # print(pos[0], pos[1])
            # print(game_over_rect)
            if (game_restart_rect.left < pos[0] < game_restart_rect.right
                    and game_restart_rect.top < pos[1] < game_restart_rect.bottom):
                self.hero.HP = 10
                self.gameover = False
            if (game_over_rect.left < pos[0] < game_over_rect.right
                    and game_over_rect.top < pos[1] < game_over_rect.bottom):
                pygame.quit()
                exit()

    # 主循环,主要处理各种事件
    def run_scene(self):

        # 播放背景音乐
        pygame.mixer.music.load('musics/bgm.mp3')
        pygame.mixer.music.play(-1)

        while True:
            # 计算元素坐标
            self.action_elements()
            # 绘制元素图片
            self.draw_elements()
            # 处理事件
            self.handle_event()
            # 碰撞检测
            self.detect_conlision()
            # 调整难度
            self.change_level()
            self.game_over()
            # 刷新显示
            pygame.display.update()
            # fpsClock.tick(FPS)


# 入口函数
if __name__ == "__main__":
    # 创建主场景
    mainScene = MainScene()
    # 开始游戏
    mainScene.run_scene()
