import sys
from os import path

import tkinter as tk
from PIL import Image, ImageTk
from random import randint

MOVE_INCREMENT = 20
moves_per_second = 10
GAME_SPEED = 1000 // moves_per_second
WIDTH = 600
HEIGHT = 620

class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width=WIDTH, height=HEIGHT, background="black", highlightthickness=0)

        self.snake_positions = [(100,100),(80,100),(60,100)]
        self.food_position = self.set_new_food_position()
        self.score = 0
        self.direction = "Right"
        self.bind_all("<Key>", self.on_key_press)

        self.load_assets()
        self.create_objects()
        self.after(GAME_SPEED, self.perform_actions)

    def load_assets(self):
        try:
            # Bundle directory... path.abspath important for --onefile export
            bundle_dir = getattr(sys, "_MEIPASS", path.abspath(path.dirname(__file__)))

            # Snake
            path_to_snake = path.join(bundle_dir, "assets", "snake.png")
            self.snake_body_image = Image.open(path_to_snake)
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            # Food
            path_to_food = path.join(bundle_dir, "assets", "food.png")
            self.food_image = Image.open(path_to_food)
            self.food = ImageTk.PhotoImage(self.food_image)
            
        except IOError as error:
            print(error)
            root.destroy()

    def create_objects(self):
        # Score Text
        self.create_text(
            100,12,text=f"Score {self.score} (Speed: {moves_per_second})", tag="score", fill="#fff", font=("TkDefaultFont",14)
        )
        # Snake Body
        for x_position, y_position in self.snake_positions:
            self.create_image(x_position,y_position,image=self.snake_body,tag="snake")
        # Food
        self.create_image(self.food_position[0], self.food_position[1], image=self.food, tag="food")

        # Rectangle (Game Boundaries)
        self.create_rectangle(7,27,593,613, outline="#EF5B3B")

    def move_snake(self):
        head_x_position, head_y_position = self.snake_positions[0]

        if self.direction == "Left":
            new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)
        elif self.direction == "Right":
            new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
        elif self.direction == "Down":
            new_head_position = (head_x_position, head_y_position + MOVE_INCREMENT)
        elif self.direction == "Up":
            new_head_position = (head_x_position, head_y_position - MOVE_INCREMENT)

        self.snake_positions = [new_head_position] + self.snake_positions[:-1]

        for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
            self.coords(segment, position)

    def perform_actions(self):
        if self.check_collisions():
            self.end_game()
            return
        self.check_food_collision()
        self.move_snake()
        self.after(GAME_SPEED, self.perform_actions)

    def check_collisions(self):
        head_x_position, head_y_position = self.snake_positions[0]

        return(
            head_x_position in (0,WIDTH)
            or head_y_position in (20,HEIGHT)
            or (head_x_position,head_y_position) in self.snake_positions[1:]
        )

    def on_key_press(self,e):
        new_direction = e.keysym
        all_directions = ("Up","Down","Left","Right")
        opposites =({"Up","Down"},{"Left","Right"})

        if (new_direction in all_directions) and {new_direction, self.direction} not in opposites:
            self.direction = new_direction

    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])

            if self.score % 5 == 0:
                global moves_per_second
                moves_per_second += 1

            self.create_image(
                *self.snake_positions[-1], image=self.snake_body, tag="snake"
            )

            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag("food"), self.food_position)

            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score: {self.score} (Speed: {moves_per_second})", tag="score")

    def set_new_food_position(self):
        while True:
            x_position = randint(1,29)*MOVE_INCREMENT
            y_position = randint(3,30)*MOVE_INCREMENT
            food_position = (x_position,y_position)

            if food_position not in self.snake_positions:
                return food_position

    def end_game(self):
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width()/2,
            self.winfo_height()/2,
            text=f"Game Over! You scored {self.score}",
            fill="#fff",
            font=("TkDefaultFont",24)
        )

# Create App
root = tk.Tk()
root.title("Snake Game")
root.resizable(False,False)

# Board
board = Snake()
board.pack()

# Run App
root.mainloop()

# ----- MAC & LINUX Deployment----- #

# (1) Export in a FOLDER (Terminal shows):
# >>> pyinstaller app.py --add-data="assets/*.png:assets"

# (2) Export in ONE FILE (Terminal shows):
# >>> pyinstaller app.py --onefile --add-data="assets/*.png:assets"

# (3) Export in a FOLDER (Terminal HIDDEN):  --->>> This one also creates a standalone!!! (BEST OPTION)
# >>> pyinstaller app.py --add-data="assets/*.png:assets" --windowed

# (4) Export in ONE FILE (Terminal HIDDEN):
# >>> pyinstaller app.py --onefile --add-data="assets/*.png:assets" --windowed


# ----- WINDOWS Deployment----- #

# (1) Export in a FOLDER (Terminal shows):
# >>> pyinstaller app.py --add-data "assets;assets"

# (2) Export in ONE FILE (Terminal shows):
# >>> pyinstaller app.py --onefile --add-data "assets;assets"

# (3) Export in a FOLDER (Terminal HIDDEN):
# >>> pyinstaller app.py --add-data "assets;assets" --windowed

# (4) Export in ONE FILE (Terminal HIDDEN):
# >>> pyinstaller app.py --onefile --add-data "assets;assets" --windowed
