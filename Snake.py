import tkinter as tk
import random

class SnakeGame(tk.Tk):
    def __init__(self, grid_size=20, cell_size=25, speed=100):
        super().__init__()
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.speed = speed

        self.title("Enhanced Snake Game")
        self.canvas_width = grid_size * cell_size
        self.canvas_height = grid_size * cell_size

        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg="black")
        self.canvas.pack()

        self.score_label = tk.Label(self, text="Score: 0", font=("Arial", 16))
        self.score_label.pack()

        self.restart_button = None

        self.init_game()

    def init_game(self):
        self.score = 0
        self.snake = [(self.grid_size // 2, self.grid_size // 2)]
        self.direction = (1, 0)
        self.food = self.create_food()
        self.running = True
        self.key_pressed = False
        self.score_label.config(text="Score: 0")
        self.canvas.delete("all")
        self.draw_snake()
        self.draw_food()
        self.bind("<KeyPress>", self.change_direction)
        self.after(self.speed, self.move_snake)

    def create_food(self):
        while True:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if (x, y) not in self.snake:
                return (x, y)

    def draw_snake(self):
        self.canvas.delete("snake")
        for i, (x, y) in enumerate(self.snake):
            color = "lime" if i == 0 else "green"
            self.canvas.create_rectangle(
                x * self.cell_size + 1, y * self.cell_size + 1,
                (x + 1) * self.cell_size - 1, (y + 1) * self.cell_size - 1,
                fill=color, tags="snake"
            )

    def draw_food(self):
        self.canvas.delete("food")
        x, y = self.food
        self.canvas.create_oval(
            x * self.cell_size + 2, y * self.cell_size + 2,
            (x + 1) * self.cell_size - 2, (y + 1) * self.cell_size - 2,
            fill="red", tags="food"
        )

    def move_snake(self):
        if not self.running:
            return

        head_x, head_y = self.snake[0]
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
        self.running = False
        self.canvas.create_text(
            self.canvas_width / 2, self.canvas_height / 2 - 20,
            text=f"Game Over!\nScore: {self.score}",
            fill="white", font=("Arial", 24)
        )

        self.restart_button = tk.Button(self, text="Restart Game", font=("Arial", 14), command=self.restart_game)
        self.restart_button.pack(pady=10)

    def restart_game(self):
        if self.restart_button:
            self.restart_button.destroy()
        self.init_game()

if __name__ == "__main__":
    game = SnakeGame()
    game.mainloop()
