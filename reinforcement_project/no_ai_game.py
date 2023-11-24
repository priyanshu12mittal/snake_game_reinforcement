import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font(r"E:\arial.ttf", 25)


class Direction(Enum):
    right = 1
    left = 2
    up = 3
    down = 4


point = namedtuple('point', 'x, y')

white = (255, 255, 255)
red = (200, 0, 0)
blue1 = (0, 100, 255)
blue2 = (0, 100, 255)
black = (0, 0, 0)

block_size = 20
speed = 40


class SnakeGameAI:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("snake")
        self.clock = pygame.time.Clock()
        self.direction = Direction.right
        self.head = point(self.w / 2, self.h / 2)

        self.snake = [self.head, point(self.head.x - block_size, self.head.y),
                      point(self.head.x - (2 * block_size), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()

    def _update_ui(self):
        self.display.fill(black)
        for pt in self.snake:
            pygame.draw.rect(self.display, blue1, pygame.Rect(pt.x, pt.y, block_size, block_size))
            pygame.draw.rect(self.display, blue2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.display, red, pygame.Rect(self.food.x, self.food.y, block_size, block_size))
        text = font.render("score : " + str(self.score), True, white)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _place_food(self):
        x = random.randint(0, (self.w - block_size) // block_size) * block_size
        y = random.randint(0, (self.h - block_size) // block_size) * block_size
        self.food = point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.left
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.right

                elif event.key == pygame.K_UP:
                    self.direction = Direction.up

                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.down
        self._move(self.direction)
        self.snake.insert(0, self.head)
        game_over = False
        if self.is_collision():
            game_over = True
            for _ in range(5):
                self._update_ui()
                pygame.display.flip()
                pygame.time.wait(200)

            return game_over, self.score

        if self.head == self.food:
            self.score += 1
            self._place_food()

            for _ in range(3):
                self._update_ui()
                pygame.display.flip()
                pygame.time.wait(100)
        else:
            self.snake.pop()

        self._update_ui()
        self.clock.tick(speed)

        return game_over, self.score

    def is_collision(self):
        if self.head.x > self.w - block_size or self.head.x < 0 or self.head.y > self.h - block_size or self.head.y < 0:
            return True

        if self.head in self.snake[1:]:
            return True

        return False

    def _move(self, direction):
        x = self.head.x
        y = self.head.y

        if self.direction == Direction.right:
            x += block_size
        elif self.direction == Direction.left:
            x -= block_size

        elif self.direction == Direction.down:
            y += block_size

        elif self.direction == Direction.up:
            y -= block_size

        for _ in range(block_size // 4):
            new_head = point(x, y)
            self.head = new_head
            self._update_ui()  # Update the display at each step of the animation
            pygame.display.flip()
            self.clock.tick(speed * 4)  # Adjust the animation speed

        self.head = point(x, y)


game = SnakeGameAI()
# Main game loop
while True:
    game_over, score = game.play_step()
    if game_over == True:
        break
print("final score", score)
pygame.quit()
