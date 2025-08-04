"""
贪吃蛇游戏

使用 `tkinter` 实现的经典贪吃蛇。通过方向键控制蛇移动，吃到食物加分并增长，撞到自己则结束。
下方为对原始英文注释的中文补充说明。
"""

import tkinter as tk
import random


class SnakeGame(tk.Tk):
    """游戏主窗口类，继承自 `tk.Tk`"""

    def __init__(self, grid_size=20, cell_size=25, speed=100):
        super().__init__()
        self.grid_size = grid_size      # 网格大小（行列数）
        self.cell_size = cell_size      # 单个格子的像素尺寸
        self.speed = speed              # 移动速度（毫秒）

        self.title("Enhanced Snake Game")
        self.canvas_width = grid_size * cell_size
        self.canvas_height = grid_size * cell_size

        # 创建画布用于显示蛇和食物
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg="black")
        self.canvas.pack()

        # 显示分数的标签
        self.score_label = tk.Label(self, text="Score: 0", font=("Arial", 16))
        self.score_label.pack()

        # 重新开始按钮（游戏结束后出现）
        self.restart_button = None

        self.init_game()  # 初始化游戏

    def init_game(self):
        """初始化或重置游戏状态"""
        self.score = 0
        self.snake = [(self.grid_size // 2, self.grid_size // 2)]  # 蛇的初始位置
        self.direction = (1, 0)                                   # 初始方向向右
        self.food = self.create_food()                            # 随机生成食物
        self.running = True                                       # 游戏运行标志
        self.key_pressed = False                                  # 防止一次循环内多次转向
        self.score_label.config(text="Score: 0")
        self.canvas.delete("all")                                 # 清空画布
        self.draw_snake()
        self.draw_food()
        self.bind("<KeyPress>", self.change_direction)           # 绑定方向键
        self.after(self.speed, self.move_snake)                   # 定时移动蛇

    def create_food(self):
        """随机生成不与蛇身重叠的食物"""
        while True:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if (x, y) not in self.snake:
                return (x, y)

    def draw_snake(self):
        """在画布上绘制蛇身"""
        self.canvas.delete("snake")
        for i, (x, y) in enumerate(self.snake):
            color = "lime" if i == 0 else "green"  # 头部用亮绿色区分
            self.canvas.create_rectangle(
                x * self.cell_size + 1, y * self.cell_size + 1,
                (x + 1) * self.cell_size - 1, (y + 1) * self.cell_size - 1,
                fill=color, tags="snake"
            )

    def draw_food(self):
        """绘制食物"""
        self.canvas.delete("food")
        x, y = self.food
        self.canvas.create_oval(
            x * self.cell_size + 2, y * self.cell_size + 2,
            (x + 1) * self.cell_size - 2, (y + 1) * self.cell_size - 2,
            fill="red", tags="food"
        )

    def move_snake(self):
        """根据当前方向移动蛇，并处理吃食物和碰撞"""
        if not self.running:
            return

        head_x, head_y = self.snake[0]
        # 通过取模实现从另一侧出现的效果
        new_head = ((head_x + self.direction[0]) % self.grid_size,
                    (head_y + self.direction[1]) % self.grid_size)

        if new_head in self.snake:
            self.game_over()
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 10
            self.score_label.config(text=f"Score: {self.score}")
            self.food = self.create_food()
            self.draw_food()
        else:
            self.snake.pop()

        self.draw_snake()
        self.key_pressed = False
        self.after(self.speed, self.move_snake)

    def change_direction(self, event):
        """响应键盘方向键事件"""
        if self.key_pressed:
            return
        self.key_pressed = True

        key = event.keysym
        if key == "Up" and self.direction != (0, 1):
            self.direction = (0, -1)
        elif key == "Down" and self.direction != (0, -1):
            self.direction = (0, 1)
        elif key == "Left" and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif key == "Right" and self.direction != (-1, 0):
            self.direction = (1, 0)

    def game_over(self):
        """游戏结束时显示提示并提供重开按钮"""
        self.running = False
        self.canvas.create_text(
            self.canvas_width / 2, self.canvas_height / 2 - 20,
            text=f"Game Over!\nScore: {self.score}",
            fill="white", font=("Arial", 24)
        )

        self.restart_button = tk.Button(
            self, text="Restart Game", font=("Arial", 14), command=self.restart_game
        )
        self.restart_button.pack(pady=10)

    def restart_game(self):
        """销毁重开按钮并重新初始化游戏"""
        if self.restart_button:
            self.restart_button.destroy()
        self.init_game()

if __name__ == "__main__":
    # 创建游戏对象并运行主循环
    game = SnakeGame()
    game.mainloop()
