import pygame
import time


def read_board(level, h, w):
    finp = open('level' + str(level) + '.txt', 'r')
    board = []
    for i in range(h):
        line = list(map(int, finp.readline().strip().split()))
        board.append(line)
    return board

pygame.init()

WIDTH, HEIGHT = 200, 50
TILE_SIZE = 24
RES_X, RES_Y = 400, 300
FPS = 30
clock = pygame.time.Clock()
screen = pygame.display.set_mode((RES_X, RES_Y))

board = read_board(1, 200, 50)

for i in range(95, 105):
    board[i][45] = 1

board[90][25] = 2

for j in range(1, 11):
    for i in range(50):
        board[j][i] = 1
        board[-j][i] = 1

tile_img = pygame.transform.scale(pygame.image.load("tile.png"), (TILE_SIZE, TILE_SIZE))
tilex_img = pygame.transform.scale(pygame.image.load("tilex.png"), (TILE_SIZE, TILE_SIZE))
background = pygame.Surface((WIDTH*TILE_SIZE, HEIGHT*TILE_SIZE))
background.fill((84, 130, 228))
for x in range(WIDTH):
    for y in range(HEIGHT):
        if board[x][y] == 1:
            background.blit(tile_img, (x * TILE_SIZE, y * TILE_SIZE))
        elif board[x][y] == 2:
            background.blit(tilex_img, (x * TILE_SIZE, y * TILE_SIZE))

class Mario:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animstate = 0
        self.speed = 6 * TILE_SIZE / FPS
        self.speed_y = 0
        self.size = 0.8
        self.state = 'sr' # s = standing, m = moving, j = jumping;   l = left, r = right
        self.stand_img_r = pygame.transform.scale(pygame.image.load("standing.png"), (int(TILE_SIZE * self.size), int(TILE_SIZE * (2 * self.size))))
        self.move_img_r = pygame.transform.scale(pygame.image.load("moving.png"), (int(TILE_SIZE * self.size), int(TILE_SIZE * (2 * self.size))))
        self.stand_img_l = pygame.transform.flip(self.stand_img_r, True, False)
        self.move_img_l = pygame.transform.flip(self.move_img_r, True, False)

    def draw(self):
        self.animstate = (self.animstate + 1) % 40
        rect = self.stand_img_r.get_rect()
        rect.center = (RES_X // 2, RES_Y // 2 + 3 * TILE_SIZE)
        if self.speed_y != 0:
            if self.state[1] == 'l':
                screen.blit(self.move_img_l, rect)
            else:
                screen.blit(self.move_img_r, rect)
        elif self.state == 'sr':
            screen.blit(self.stand_img_r, rect)
        elif self.state == 'sl':
            screen.blit(self.stand_img_l, rect)
        elif self.state[0] == 'm':
            if (self.animstate % 20) < 10:
                if self.state[1] == 'r':
                    screen.blit(self.stand_img_r, rect)
                else:
                    screen.blit(self.stand_img_l, rect)
            else:
                if self.state[1] == 'r':
                    screen.blit(self.move_img_r, rect)
                else:
                    screen.blit(self.move_img_l, rect)

    def move(self, state=None):
        if state == None:
            state = 's' + self.state[1]
        self.state = state
        self.speed_y += 0.5
        if board[int(self.x / TILE_SIZE)][int(self.y / TILE_SIZE + self.size)] == 1:
            self.y = TILE_SIZE * int(self.y / TILE_SIZE) + TILE_SIZE * (1 - self.size)
            self.speed_y = 0
        elif board[int(self.x / TILE_SIZE)][int(self.y / TILE_SIZE - self.size)] == 1:
            self.y = TILE_SIZE * int(self.y / TILE_SIZE + (1 - self.size)) + self.size * TILE_SIZE
            self.speed_y = 0.0356856747
        self.y += self.speed_y
        if self.state == 'mr':
            if board[int((self.x + self.speed) / TILE_SIZE + (self.size / 2))][int(self.y / TILE_SIZE + (self.size * 0.6))] == 1 \
            or board[int((self.x + self.speed) / TILE_SIZE + (self.size / 2))][int(self.y / TILE_SIZE - (self.size * 0.6))] == 1:
                self.x = TILE_SIZE * int((self.x + self.speed) / TILE_SIZE + (self.size / 2)) - (self.size / 2) * TILE_SIZE
            else:
                self.x += self.speed
        elif self.state == 'ml':
            if board[int((self.x - self.speed) / TILE_SIZE - (self.size / 2))][int(self.y / TILE_SIZE + (self.size * 0.6))] == 1 \
            or board[int((self.x - self.speed) / TILE_SIZE - (self.size / 2))][int(self.y / TILE_SIZE - (self.size * 0.6))] == 1:
                self.x = TILE_SIZE * int((self.x - self.speed) / TILE_SIZE - (self.size / 2)) + 1.4 * TILE_SIZE
            else:
                self.x -= self.speed


        if board[int(self.x / TILE_SIZE)][int(self.y / TILE_SIZE + self.size)] == 2:
            return True
        elif board[int(self.x / TILE_SIZE)][int(self.y / TILE_SIZE - self.size)] == 2:
            return True
        if self.state == 'mr':
            if board[int((self.x + self.speed) / TILE_SIZE + (self.size / 2))][int(self.y / TILE_SIZE + (self.size * 0.6))] == 2 \
            or board[int((self.x + self.speed) / TILE_SIZE + (self.size / 2))][int(self.y / TILE_SIZE - (self.size * 0.6))] == 2:
                return True
        elif self.state == 'ml':
            if board[int((self.x - self.speed) / TILE_SIZE - (self.size / 2))][int(self.y / TILE_SIZE + (self.size * 0.6))] == 2 \
            or board[int((self.x - self.speed) / TILE_SIZE - (self.size / 2))][int(self.y / TILE_SIZE - (self.size * 0.6))] == 2:
                return True

    def jump(self):
        if self.speed_y == 0:
            self.y -= self.speed
            self.speed_y = -2.084794 * self.speed

def start_game(level):
    global m, f, running, playing, pause, LEVEL, BLOCKS, sp
    global TILE_SIZE, RES_X, RES_Y, WIDTH, HEIGHT, screen, FPS, clock, screen, board, tile_img, tilex_img, background
    m = Mario(TILE_SIZE * 100, 0)
    running = True

    pause = False

    LEVEL = level
    BLOCKS = 10
    sp = - 1

    WIDTH, HEIGHT = 200, 50
    TILE_SIZE = 24
    RES_X, RES_Y = 400, 300
    FPS = 30
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((RES_X, RES_Y))

    board = read_board(LEVEL, 200, 50)

    for i in range(95, 105):
        board[i][45] = 1

    for j in range(1, 11):
        for i in range(50):
            board[j][i] = 1
            board[-j][i] = 1

    if LEVEL == 1:
        board[90][10] = 2
    elif LEVEL == 2:
        board[90][10] = 2
    elif LEVEL == 3:
        board[114][9] = 2
    tilex_img = pygame.transform.scale(pygame.image.load("tilex.png"), (TILE_SIZE, TILE_SIZE))
    tile_img = pygame.transform.scale(pygame.image.load("tile.png"), (TILE_SIZE, TILE_SIZE))
    background = pygame.Surface((WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE))
    background.fill((84, 130, 228))
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if board[x][y] == 1:
                background.blit(tile_img, (x * TILE_SIZE, y * TILE_SIZE))
            if board[x][y] == 2:
                background.blit(tilex_img, (x * TILE_SIZE, y * TILE_SIZE))
    textsurface1 = font1.render(str("CHOOSE"), False, pygame.Color('green'))
    textsurface2 = font1.render(str("LEVEL"), False, pygame.Color('green'))

    screen.fill((84, 130, 228))
    choose = [font2.render(str("level " + str(i + 1)), False, pygame.Color('green')) for i in range(8)]
    for i in range(8):
        screen.blit(choose[i], (170, yst + i * 23))

    screen.blit(textsurface1, (123, 20))
    screen.blit(textsurface2, (148, 60))

m = Mario(TILE_SIZE * 100, 0)
running = True

playing = False
pause = False
won = False

font1 = pygame.font.SysFont('Arial', 40)
font2 = pygame.font.SysFont('Arial', 22)
font3 = pygame.font.SysFont('Arial', 23)

LEVEL = None
BLOCKS = 10
sp = - 1

mp = None
while running:
    if not playing:
        sp = -1
        screen.fill((84, 130, 228))
        textsurface1 = font1.render(str("CHOOSE"), False, pygame.Color('green'))
        textsurface2 = font1.render(str("LEVEL"), False, pygame.Color('green'))

        choose = [font2.render(str("level " + str(i + 1)), False, pygame.Color('green')) for i in range(8)]

        yst = 110

        mp = pygame.mouse.get_pos()

        if mp is not None:
            if 170 <= mp[0] <= 223:
                sp = (mp[1] - 110) // 23
                if 0 <= sp <= 7:
                    choose[sp] = font2.render(str("level " + str(sp + 1)), False, pygame.Color('red'))
        else:
            sp = -1

        for i in range(8):
            screen.blit(choose[i], (170, yst + i * 23))

        screen.blit(textsurface1, (123, 20))
        screen.blit(textsurface2, (148, 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and 0 <= sp <= 7:
                playing = True
                LEVEL = sp
                start_game(sp + 1)

        pygame.display.flip()
        continue

    if pause:
        md = False
        if won:
            ts2 = font1.render(str("NICELY DONE"), False, pygame.Color('green'))
        else:
            ts2 = None

        ts0 = font1.render(str("CONTINUE"), False, pygame.Color('green'))
        ts1 = font1.render(str("EXIT"), False, pygame.Color('green'))

        mp = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                md = True

        if mp is not None:
            if 120 <= mp[0] <= 290 and 50 <= mp[1] <= 87:
                ts0 = font1.render(str("CONTINUE"), False, pygame.Color('red'))
                if md:
                    pause = False
            elif 170 <= mp[0] <= 250 and 90 <= mp[1] <= 130:
                ts1 = font1.render(str("EXIT"), False, pygame.Color('red'))
                if md:
                    pause = False
                    playing = False

        screen.blit(ts0, (120, 50))
        screen.blit(ts1, (170, 90))
        if ts2 is not None:
            screen.blit(ts2, (100, 0))
        pygame.display.flip()

        continue


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and BLOCKS > 0:
            mp = pygame.mouse.get_pos()
            a, b = (RES_X // 2 - int(m.x), RES_Y // 2 + 3 * TILE_SIZE - int(m.y))
            xp, yp = (mp[0] - a) // TILE_SIZE * TILE_SIZE, (mp[1] - b) // TILE_SIZE * TILE_SIZE
            print([xp // TILE_SIZE, yp // TILE_SIZE])
            if board[xp // TILE_SIZE][yp // TILE_SIZE] not in (1, 2):
                board[xp // TILE_SIZE][yp // TILE_SIZE] = 1
                background.blit(tile_img, (xp, yp))
                BLOCKS -= 1
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        pause = True
    if pygame.key.get_pressed()[pygame.K_UP]:
        m.jump()
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        if m.move('mr'):
            pause = True
            won = True
    elif pygame.key.get_pressed()[pygame.K_LEFT]:
        if m.move('ml'):
            pause = True
            won = True
    else:
        m.move()

    ts = font3.render(str("BLOCKS: " + str(BLOCKS)), False, pygame.Color('red'))

    screen.blit(background, (RES_X // 2 - int(m.x), RES_Y // 2 + 3 * TILE_SIZE - int(m.y)))
    m.draw()
    screen.blit(ts, (280, 0))
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
