"""
俄罗斯方块游戏

使用 `pygame` 实现的简易俄罗斯方块。方块自上而下落下，玩家通过方向键移动或旋转方块，填满一行即可消除并得分。
以下为对原代码的中文注释，帮助理解实现细节。
"""

import pygame
import random
import time
import sys

# 初始化 pygame
pygame.init()

# 常量设置
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600  # 屏幕宽高
BLOCK_SIZE = 30                         # 单个方块像素大小
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
FPS = 60                               # 刷新帧率

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 191, 255)
GRAY = (200, 200, 200)

SHAPES = [
    [[1, 1, 1, 1]],  # I 形方块
    [[1, 1], [1, 1]],  # O 形方块
    [[0, 1, 0], [1, 1, 1]],  # T 形方块
    [[1, 1, 0], [0, 1, 1]],  # S 形方块
    [[0, 1, 1], [1, 1, 0]],  # Z 形方块
    [[1, 0, 0], [1, 1, 1]],  # L 形方块
    [[0, 0, 1], [1, 1, 1]]   # J 形方块
]
COLORS = [CYAN, YELLOW, PURPLE, GREEN, RED, BLUE, LIGHT_BLUE]

# 创建窗口并设置标题
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

class Tetris:
    """核心游戏逻辑类"""

    def __init__(self):
        self.reset()  # 初始化游戏状态

    def reset(self):
        """重置棋盘和游戏参数"""
        self.board = [[BLACK] * GRID_WIDTH for _ in range(GRID_HEIGHT)]  # 游戏网格
        self.clock = pygame.time.Clock()
        self.fall_speed = 500             # 方块下落速度（毫秒）
        self.last_fall_time = time.time()
        self.score = 0
        self.game_over = False
        self.current_piece = None
        self.next_piece = self.get_random_piece()
        self.new_piece()

    def get_random_piece(self):
        """随机选择一个方块及其颜色"""
        index = random.randint(0, len(SHAPES) - 1)
        return SHAPES[index], COLORS[index]

    def new_piece(self):
        """生成新的当前方块并检查是否立即碰撞"""
        self.current_piece, self.current_color = self.next_piece
        self.current_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.current_y = 0
        self.next_piece = self.get_random_piece()
        if self.check_collision():
            self.game_over = True

    def draw_board(self):
        """绘制已经固定的方块"""
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(
                    screen, self.board[y][x],
                    (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                )
                pygame.draw.rect(
                    screen, WHITE,
                    (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1
                )

    def draw_piece(self):
        """绘制当前正在下落的方块"""
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen, self.current_color,
                        ((self.current_x + x) * BLOCK_SIZE, (self.current_y + y) * BLOCK_SIZE,
                         BLOCK_SIZE, BLOCK_SIZE)
                    )

    def check_collision(self, offset_x=0, offset_y=0):
        """检测移动或旋转后是否发生碰撞"""
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    nx = self.current_x + x + offset_x
                    ny = self.current_y + y + offset_y
                    if nx < 0 or nx >= GRID_WIDTH or ny >= GRID_HEIGHT:
                        return True
                    if ny >= 0 and self.board[ny][nx] != BLACK:
                        return True
        return False

    def lock_piece(self):
        """将当前方块固定到棋盘上"""
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.current_y + y][self.current_x + x] = self.current_color

    def clear_lines(self):
        """检查并清除完整的行，同时更新得分"""
        self.board = [row for row in self.board if any(cell == BLACK for cell in row)]
        lines_cleared = GRID_HEIGHT - len(self.board)
        for _ in range(lines_cleared):
            self.board.insert(0, [BLACK] * GRID_WIDTH)
        self.score += lines_cleared

    def rotate_piece(self):
        """顺时针旋转当前方块"""
        rotated = [list(row) for row in zip(*self.current_piece[::-1])]
        old_piece = self.current_piece
        self.current_piece = rotated
        if self.check_collision():
            self.current_piece = old_piece  # 发生碰撞则还原

    def move_left(self):
        """向左移动当前方块"""
        if not self.check_collision(offset_x=-1):
            self.current_x -= 1

    def move_right(self):
        """向右移动当前方块"""
        if not self.check_collision(offset_x=1):
            self.current_x += 1

    def move_down(self):
        """向下移动当前方块，若到底则锁定并生成新方块"""
        if not self.check_collision(offset_y=1):
            self.current_y += 1
        else:
            self.lock_piece()
            self.clear_lines()
            self.new_piece()

    def update(self):
        """根据时间控制方块自动下落"""
        if not self.game_over:
            if time.time() - self.last_fall_time > self.fall_speed / 1000:
                self.move_down()
                self.last_fall_time = time.time()

    def handle_events(self):
        """处理用户输入和窗口事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if not self.game_over:
                    if event.key == pygame.K_LEFT:
                        self.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.move_right()
                    elif event.key == pygame.K_DOWN:
                        self.move_down()
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()

            elif event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                if self.restart_button.collidepoint(event.pos):
                    self.reset()

    def draw_game_over(self):
        """绘制游戏结束界面及重开按钮"""
        font = pygame.font.SysFont("Arial", 28)
        msg = font.render("Game Over!", True, WHITE)
        restart = font.render("Restart", True, BLACK)

        msg_rect = msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2, 120, 40)

        pygame.draw.rect(screen, GRAY, self.restart_button)
        pygame.draw.rect(screen, WHITE, self.restart_button, 2)
        screen.blit(msg, msg_rect)
        screen.blit(restart, restart.get_rect(center=self.restart_button.center))

    def run(self):
        """主循环，负责更新和渲染"""
        while True:
            screen.fill(BLACK)
            self.handle_events()
            self.update()

            self.draw_board()
            if not self.game_over:
                self.draw_piece()
            else:
                self.draw_game_over()

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Tetris()
    game.run()
