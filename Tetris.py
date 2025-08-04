import pygame
import random
import time
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
FPS = 60

# Colors
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
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]]   # J
]
COLORS = [CYAN, YELLOW, PURPLE, GREEN, RED, BLUE, LIGHT_BLUE]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

class Tetris:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [[BLACK] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.clock = pygame.time.Clock()
        self.fall_speed = 500
        self.last_fall_time = time.time()
        self.score = 0
        self.game_over = False
        self.current_piece = None
        self.next_piece = self.get_random_piece()
        self.new_piece()

    def get_random_piece(self):
        index = random.randint(0, len(SHAPES) - 1)
        return SHAPES[index], COLORS[index]

    def new_piece(self):
        self.current_piece, self.current_color = self.next_piece
        self.current_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.current_y = 0
        self.next_piece = self.get_random_piece()
        if self.check_collision():
            self.game_over = True

    def draw_board(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(screen, self.board[y][x],
                                 (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, WHITE,
                                 (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_piece(self):
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.current_color,
                                     ((self.current_x + x) * BLOCK_SIZE, (self.current_y + y) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))

    def check_collision(self, offset_x=0, offset_y=0):
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
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.current_y + y][self.current_x + x] = self.current_color

    def clear_lines(self):
        self.board = [row for row in self.board if any(cell == BLACK for cell in row)]
        lines_cleared = GRID_HEIGHT - len(self.board)
        for _ in range(lines_cleared):
            self.board.insert(0, [BLACK] * GRID_WIDTH)
        self.score += lines_cleared

    def rotate_piece(self):
        rotated = [list(row) for row in zip(*self.current_piece[::-1])]
        old_piece = self.current_piece
        self.current_piece = rotated
        if self.check_collision():
            self.current_piece = old_piece  # Revert

    def move_left(self):
        if not self.check_collision(offset_x=-1):
            self.current_x -= 1

    def move_right(self):
        if not self.check_collision(offset_x=1):
            self.current_x += 1

    def move_down(self):
        if not self.check_collision(offset_y=1):
            self.current_y += 1
        else:
            self.lock_piece()
            self.clear_lines()
            self.new_piece()

    def update(self):
        if not self.game_over:
            if time.time() - self.last_fall_time > self.fall_speed / 1000:
                self.move_down()
                self.last_fall_time = time.time()

    def handle_events(self):
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
