"""
水排序小游戏（Water Sort）

此脚本使用 `pygame` 框架实现一个颜色排序的益智游戏。
玩家通过点击不同试管中的彩色球，将相同颜色的球全部集中在同一试管中。
当所有非空试管都只包含一种颜色且装满时，游戏胜利。

主要功能：
- 随机生成带有彩色球的试管棋盘。
- 支持鼠标选择和移动球体。
- 检查玩家是否成功完成排序。

作者原注释为英文，为方便中文读者理解，在此添加详细中文注释。
"""

# 导入关键模块：random 用于棋盘生成，copy 用于重开时复制状态，pygame 为游戏框架
import copy
import random
import pygame

# 初始化 pygame
pygame.init()

# 初始化游戏变量
WIDTH = 500
HEIGHT = 550
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Water Sort PyGame')
font = pygame.font.Font('freesansbold.ttf', 24)
fps = 60
timer = pygame.time.Clock()
color_choices = ['red', 'orange', 'light blue', 'dark blue', 'dark green', 'pink', 'purple', 'dark gray',
                 'brown', 'light green', 'yellow', 'white']
tube_colors = []
initial_colors = []
# 10 - 14 tubes, always start with two empty
tubes = 10
new_game = True
selected = False
tube_rects = []
select_rect = 100
win = False



# 在新游戏开始时随机生成试管数量并随机分配颜色
def generate_start():
    tubes_number = random.randint(10, 14)
    tubes_colors = []
    available_colors = []
    for i in range(tubes_number):
        tubes_colors.append([])
        if i < tubes_number - 2:
            for j in range(4):
                available_colors.append(i)
    for i in range(tubes_number - 2):
        for j in range(4):
            color = random.choice(available_colors)
            tubes_colors[i].append(color)
            available_colors.remove(color)
    print(tubes_colors)
    print(tubes_number)
    return tubes_number, tubes_colors


# 绘制所有试管及其中的颜色，同时标识当前被选中的试管
def draw_tubes(tubes_num, tube_cols):
    tube_boxes = []
    if tubes_num % 2 == 0:
        tubes_per_row = tubes_num // 2
        offset = False
    else:
        tubes_per_row = tubes_num // 2 + 1
        offset = True
    spacing = WIDTH / tubes_per_row

    # Draw tubes and then circles inside them
    for i in range(tubes_per_row):
        # Draw tube outline
        box = pygame.draw.rect(screen, 'blue', [5 + spacing * i, 50, 65, 200], 5, 5)
        if select_rect == i:
            pygame.draw.rect(screen, 'green', [5 + spacing * i, 50, 65, 200], 3, 5)
        tube_boxes.append(box)

        # Draw circles for colors inside the tube
        for j in range(len(tube_cols[i])):
            pygame.draw.circle(screen, color_choices[tube_cols[i][j]], 
                               (5 + spacing * i + 32, 200 - (50 * j) + 25), 20)

    if offset:
        for i in range(tubes_per_row - 1):
            box = pygame.draw.rect(screen, 'blue', [(spacing * 0.5) + 5 + spacing * i, 300, 65, 200], 5, 5)
            if select_rect == i + tubes_per_row:
                pygame.draw.rect(screen, 'green', [(spacing * 0.5) + 5 + spacing * i, 300, 65, 200], 3, 5)
            tube_boxes.append(box)

            for j in range(len(tube_cols[i + tubes_per_row])):
                pygame.draw.circle(screen, color_choices[tube_cols[i + tubes_per_row][j]], 
                                   ((spacing * 0.5) + 5 + spacing * i + 32, 450 - (50 * j) + 25), 20)

    else:
        for i in range(tubes_per_row):
            box = pygame.draw.rect(screen, 'blue', [5 + spacing * i, 300, 65, 200], 5, 5)
            if select_rect == i + tubes_per_row:
                pygame.draw.rect(screen, 'green', [5 + spacing * i, 300, 65, 200], 3, 5)
            tube_boxes.append(box)

            for j in range(len(tube_cols[i + tubes_per_row])):
                pygame.draw.circle(screen, color_choices[tube_cols[i + tubes_per_row][j]], 
                                   (5 + spacing * i + 32, 450 - (50 * j) + 25), 20)

    return tube_boxes


# 根据当前选择的试管和目标试管，计算可以移动的颜色及数量
def calc_move(colors, selected_rect, destination):
    chain = True
    color_on_top = 100
    length = 1
    color_to_move = 100
    if len(colors[selected_rect]) > 0:
        color_to_move = colors[selected_rect][-1]
        for i in range(1, len(colors[selected_rect])):
            if chain:
                if colors[selected_rect][-1 - i] == color_to_move:
                    length += 1
                else:
                    chain = False
    if 4 > len(colors[destination]):
        if len(colors[destination]) == 0:
            color_on_top = color_to_move
        else:
            color_on_top = colors[destination][-1]
    if color_on_top == color_to_move:
        for i in range(length):
            if len(colors[destination]) < 4:
                if len(colors[selected_rect]) > 0:
                    colors[destination].append(color_on_top)
                    colors[selected_rect].pop(-1)
    print(colors, length)
    return colors


# 检查是否所有非空试管都被同一颜色填满四个球，满足则胜利
def check_victory(colors):
    won = True
    for i in range(len(colors)):
        if len(colors[i]) > 0:
            if len(colors[i]) != 4:
                won = False
            else:
                main_color = colors[i][-1]
                for j in range(len(colors[i])):
                    if colors[i][j] != main_color:
                        won = False
    return won


# 主游戏循环
run = True
while run:
    screen.fill('black')
    timer.tick(fps)
    # 当开始新游戏时生成棋盘，并复制初始颜色以便重新开始
    if new_game:
        tubes, tube_colors = generate_start()
        initial_colors = copy.deepcopy(tube_colors)
        new_game = False
    # 每帧绘制所有试管
    else:
        tube_rects = draw_tubes(tubes, tube_colors)
    # 每帧检查是否已经胜利
    win = check_victory(tube_colors)
    # 事件处理：退出、点击选择试管、空格重玩、回车生成新棋盘
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                tube_colors = copy.deepcopy(initial_colors)
            elif event.key == pygame.K_RETURN:
                new_game = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not selected:
                for item in range(len(tube_rects)):
                    if tube_rects[item].collidepoint(event.pos):
                        selected = True
                        select_rect = item
            else:
                for item in range(len(tube_rects)):
                    if tube_rects[item].collidepoint(event.pos):
                        dest_rect = item
                        tube_colors = calc_move(tube_colors, select_rect, dest_rect)
                        selected = False
                        select_rect = 100
    # 如果胜利则在屏幕中间显示提示；顶部始终显示重玩和新棋盘提示
    if win:
        victory_text = font.render('You Won! Press Enter for a new board!', True, 'white')
        screen.blit(victory_text, (30, 265))
    restart_text = font.render('Stuck? Space-Restart, Enter-New Board!', True, 'white')
    screen.blit(restart_text, (10, 10))

    # 刷新屏幕显示所有内容；若 run 为 False 则退出 pygame
    pygame.display.flip()

# 退出 pygame
pygame.quit()
