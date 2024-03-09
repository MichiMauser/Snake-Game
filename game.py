import random
import time
from tkinter import *
from game_misc import *


class Snake:
    def __init__(self):
        self.body_size = SNAKE_BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, SNAKE_BODY_PARTS):
            self.coordinates.append([50, 50])
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SIZE, y + SIZE, fill=SNAKE_COLOR, tags='snake')
            self.squares.append(square)


class Food:

    def __init__(self):
        coord_x = random.randint(0, int(GAME_WIDTH / SIZE) - 1) * SIZE
        coord_y = random.randint(0, int(GAME_HEIGHT / SIZE) - 1) * SIZE
        self.coord = [coord_x, coord_y]

        canvas.create_rectangle(coord_x, coord_y, coord_x + SIZE, coord_y + SIZE, fill=FOOD_COLOR, tags='food')


def next_turn(snake, food):
    coord_x, coord_y = snake.coordinates[0]
    if direction == 'up':
        coord_y -= SIZE
    elif direction == 'down':
        coord_y += SIZE
    elif direction == 'right':
        coord_x += SIZE
    elif direction == 'left':
        coord_x -= SIZE

    food_x, food_y = food.coord
    if food_x == coord_x and food_y == coord_y:
        global SCORE
        SCORE += 1
        label.config(text=f"Score is {SCORE}")
        canvas.delete('food')
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    snake.coordinates.insert(0, (coord_x, coord_y))
    square = canvas.create_rectangle(coord_x, coord_y, coord_x + SIZE, coord_y + SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if check_collision(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_dir(new_dir):
    global direction
    if new_dir == 'left':
        if direction != 'right':
            direction = new_dir

    elif new_dir == 'right':
        if direction != 'left':
            direction = new_dir

    elif new_dir == 'up':
        if direction != 'down':
            direction = new_dir

    elif new_dir == 'down':
        if direction != 'up':
            direction = new_dir


def check_collision(snake) -> bool:
    x_coord, y_coord = snake.coordinates[0]
    if x_coord < 0 or x_coord >= GAME_WIDTH or y_coord < 0 or y_coord >= GAME_HEIGHT:
        print("GAME OVER")
        return True

    for body_coord in snake.coordinates[1::]:
        if x_coord == body_coord[0] and y_coord == body_coord[1]:
            print("GAME OVER")
            return True


def game_over():
    canvas.delete(ALL)
    canvas.create_text(250, 250, font=('Comic Sans MS', 50), text="GAME OVER", fill="Blue", tags="game over")


window = Tk()
window.title('The Snake')
window.resizable(False, False)

label = Label(text=f"Score is {SCORE}", font=('Comic Sans MS', 20))
label.pack()

canvas = Canvas(window, height=GAME_HEIGHT, width=GAME_WIDTH, background=BACKGROUND_COLOR)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window.eval('tk::PlaceWindow . center')
window.bind('<Left>', lambda event: change_dir('left'))
window.bind('<Right>', lambda event: change_dir('right'))
window.bind('<Up>', lambda event: change_dir('up'))
window.bind('<Down>', lambda event: change_dir('down'))

snake = Snake()
food = Food()
next_turn(snake, food)

window.mainloop()
