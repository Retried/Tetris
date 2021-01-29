import pygame
import random
from pygame import mixer

level = 2
width = 500
height = 500

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
PURPLE = (138, 43, 226)

colors = [
    None,
    CYAN,
    RED,
    GREEN,
    BLUE,
    ORANGE,
    PURPLE,
    YELLOW,
]


class Menu:

    def __init__(self):
        menu = True

        global level

        while menu:
            for event1 in pygame.event.get():
                if event1.type == pygame.QUIT:
                    pygame.quit()
                if event1.type == pygame.KEYDOWN:
                    if event1.key == pygame.K_UP:
                        if level > 1:
                            level -= 1
                    elif event1.key == pygame.K_DOWN:
                        if level < 3:
                            level += 1
                    if event1.key == pygame.K_RETURN:
                        menu = False
                        break

            screen.fill(BLACK)
            text_menu = font2.render("Choose difficulty:", True, BLUE)
            if level == 1:
                text_easy = font.render("Easy", True, WHITE)
            else:
                text_easy = font.render("Easy", True, GRAY)
            if level == 2:
                text_normal = font.render("Normal", True, WHITE)
            else:
                text_normal = font.render("Normal", True, GRAY)
            if level == 3:
                text_hard = font.render("Hard", True, WHITE)
            else:
                text_hard = font.render("Hard", True, GRAY)

            menu_rect = text_menu.get_rect()
            easy_rect = text_easy.get_rect()
            normal_rect = text_normal.get_rect()
            hard_rect = text_hard.get_rect()

            screen.blit(text_menu, (width / 2 - (menu_rect[2] / 2), 150))
            screen.blit(text_easy, (width / 2 - (easy_rect[2] / 2), 200))
            screen.blit(text_normal, (width / 2 - (normal_rect[2] / 2), 225))
            screen.blit(text_hard, (width / 2 - (hard_rect[2] / 2), 250))
            pygame.display.update()
            clock.tick(fps)


class Figure:
    tetromino = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self):
        self.x = 3
        self.y = 0
        self.type = random.randint(0, len(self.tetromino) - 1)
        self.color = self.type + 1
        self.rotation = 0

    def image(self):
        return self.tetromino[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.tetromino[self.type])


class Tetris:
    score = 0
    state = "start"
    field = []
    x = 100
    y = 60
    zoom = 20
    new = Figure()
    figure = new
    while figure.type == new.type:
        new = Figure()

    def __init__(self, h, w):
        self.height = h
        self.width = w
        self.field = []
        self.score = 0
        self.state = "start"
        for i1 in range(height):
            new_line = []
            for j1 in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        self.figure = self.new
        while game.figure.type == game.new.type:
            self.new = Figure()

    def intersects(self):
        intersection = False
        for i2 in range(4):
            for j2 in range(4):
                if i2 * 4 + j2 in self.figure.image():
                    if i2 + self.figure.y > self.height - 1 or \
                            j2 + self.figure.x > self.width - 1 or \
                            j2 + self.figure.x < 0 or \
                            self.field[i2 + self.figure.y][j2 + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i3 in range(1, self.height):
            zeros = 0
            for j3 in range(self.width):
                if self.field[i3][j3] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 10
                for k3 in range(i3, 1, -1):
                    for j3 in range(self.width):
                        self.field[k3][j3] = self.field[k3 - 1][j3]
        self.score += lines ** 2

    def space(self):
        if game.state != "gameover":
            while not self.intersects():
                self.figure.y += 1
            self.figure.y -= 1
            self.freeze()

    def down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i4 in range(4):
            for j4 in range(4):
                if i4 * 4 + j4 in self.figure.image():
                    self.field[i4 + self.figure.y][j4 + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def move_side(self, dx):
        move_sound = mixer.Sound("sounds\\move.wav")
        mixer.Sound.set_volume(move_sound, 0.04)
        if game.state != "gameover":
            old_x = self.figure.x
            self.figure.x += dx
            if self.intersects():
                self.figure.x = old_x
            move_sound.play()

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

    @staticmethod
    def music():
        mixer.music.set_volume(0.04)
        mixer.music.load("sounds\\music.mp3")
        mixer.music.play(-1)


pygame.init()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris")

font = pygame.font.SysFont('Calibri', 25, True, False)
font1 = pygame.font.SysFont('Calibri', 50, True, False)
font2 = pygame.font.SysFont('Calibri', 35, True, False)

done = False
clock = pygame.time.Clock()
fps = 25
Menu()
game = Tetris(20, 10)
game.music()
go = mixer.Sound("sounds\\clear.wav")
mixer.Sound.set_volume(go, 0.04)
counter = 0
stop = 1

pressing_down = False

while not done:
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.down()

    for event2 in pygame.event.get():
        if event2.type == pygame.QUIT:
            done = True
        if event2.type == pygame.KEYDOWN:
            if event2.key == pygame.K_UP:
                game.rotate()
            elif event2.key == pygame.K_DOWN:
                pressing_down = True
            elif event2.key == pygame.K_LEFT:
                game.move_side(-1)
            elif event2.key == pygame.K_RIGHT:
                game.move_side(1)
            elif event2.key == pygame.K_SPACE:
                game.space()
            elif event2.key == pygame.K_ESCAPE and game.state == "gameover":
                stop = 1
                game.music()
                game.__init__(20, 10)

        if event2.type == pygame.KEYUP:
            if event2.key == pygame.K_DOWN:
                pressing_down = False

    screen.fill(BLACK)

    for i5 in range(game.height):
        for j5 in range(game.width):
            pygame.draw.rect(screen, GRAY,
                             [game.x + game.zoom * j5,
                              game.y + game.zoom * i5,
                              game.zoom, game.zoom], border_radius=3)
            if game.field[i5][j5] > 0:
                pygame.draw.rect(screen, colors[game.field[i5][j5]],
                                 [game.x + game.zoom * j5 + 1,
                                  game.y + game.zoom * i5 + 1,
                                  game.zoom - 1, game.zoom - 1])

    if game.figure is not None:
        for i6 in range(4):
            for j6 in range(4):
                p = i6 * 4 + j6
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j6 + game.figure.x) + 1,
                                      game.y + game.zoom * (i6 + game.figure.y) + 1,
                                      game.zoom - 1, game.zoom - 1])
                if p in game.new.image():
                    pygame.draw.rect(screen, colors[game.new.color],
                                     [game.x * 3 + game.zoom * (j6 + game.new.x),
                                      game.y * 2.5 + game.zoom * (i6 + game.new.x),
                                      game.zoom - 1, game.zoom - 1])

    score_text = font.render("Your Score:", True, WHITE)
    points_text = font.render(str(game.score), True, WHITE)
    shape_text = font.render("Next shape: ", True, WHITE)
    sp_text = font.render("Your Score: " + str(game.score), True, WHITE)
    go_text1 = font1.render("Game Over", True, ORANGE)
    go_text2 = font1.render("Press ESC to reset", True, YELLOW)

    text_rect = score_text.get_rect()
    score_rect = points_text.get_rect()
    next_rect = shape_text.get_rect()
    go_rect = go_text1.get_rect()
    score2_rect = sp_text.get_rect()
    go1_rect = go_text2.get_rect()

    screen.blit(score_text, [400 - (text_rect[2] / 2), 100])
    screen.blit(points_text, [400 - (score_rect[2] / 2), 120])
    screen.blit(shape_text, [400 - (next_rect[2] / 2), 175])
    if game.state == "gameover":
        screen.fill(BLACK)
        screen.blit(go_text1, [(width / 2 - (go_rect[2] / 2)), 200])
        screen.blit(sp_text, [(width / 2 - (score2_rect[2] / 2)), 250])
        screen.blit(go_text2, [(width / 2 - (go1_rect[2] / 2)), 275])
        mixer.music.stop()
        if stop == 1:
            go.play()
            stop = 0
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
