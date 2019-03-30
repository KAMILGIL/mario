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
board = [[0] * (HEIGHT - int(((i - 100) / 20) ** 2) // 2 - 2) + [1] * (int(((i - 100) / 20) ** 2) // 2 + 2) for i in range(WIDTH)]


#board = read_board(1, 200, 50)
for i in range(95, 105):
    board[i][30] = 1

for j in range(40, 80):
    for i in range(50):
        board[j][i] = 1
        board[-j][i] = 1

tile_img = pygame.transform.scale(pygame.image.load("tile.png"), (TILE_SIZE, TILE_SIZE))
background = pygame.Surface((WIDTH*TILE_SIZE, HEIGHT*TILE_SIZE))
background.fill((84, 130, 228))
for x in range(WIDTH):
    for y in range(HEIGHT):
        if board[x][y] == 1:
            background.blit(tile_img, (x * TILE_SIZE, y * TILE_SIZE))
            print((x * TILE_SIZE, y * TILE_SIZE), "TILE")

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

    def jump(self):
        if self.speed_y == 0:
            self.y -= self.speed
            self.speed_y = -2.084794 * self.speed


class Flower:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animstate = 0
        self.size = 0.8
        self.image = pygame.transform.scale(pygame.image.load("flower.png"), (int(TILE_SIZE * self.size), int(TILE_SIZE * (2 * self.size))))

    def draw(self):
        self.animstate = (self.animstate + 1) % (3 * FPS)
        offset = int(abs(self.animstate - 1.5 * FPS) / (1.5 * FPS) * 4 * TILE_SIZE)
        rect = self.image.get_rect()
        rect.center = ((self.x + (self.size / 2)) * TILE_SIZE - int(m.x), self.y * TILE_SIZE - int(m.y) + offset)
        screen.blit(self.image, rect)



m = Mario(TILE_SIZE * 100, 0)
f = Flower(97, 28)
running = True

mp = None
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mp = pygame.mouse.get_pos()
            a, b = (RES_X // 2 - int(m.x), RES_Y // 2 + 3 * TILE_SIZE - int(m.y))
            xp, yp = (mp[0] - a) // TILE_SIZE * TILE_SIZE, (mp[1] - b) // TILE_SIZE * TILE_SIZE
            board[xp // TILE_SIZE][yp // TILE_SIZE] = 1
            print(xp // TILE_SIZE,
                  yp // TILE_SIZE)
            background.blit(tile_img, (xp, yp))
        if event.type == pygame.KEYDOWN:
            if pygame.key == pygame.K_q:
                mp = pygame.mouse.get_pos()
                if mp is not None:
                    print("KONCH")
                    a, b = (RES_X // 2 - int(m.x), RES_Y // 2 + 3 * TILE_SIZE - int(m.y))
                    xp, yp = (mp[0] - a) // TILE_SIZE * TILE_SIZE, (mp[1] - b) // TILE_SIZE * TILE_SIZE
                    board[xp // TILE_SIZE][yp // TILE_SIZE] = 2
                    print(xp // TILE_SIZE,
                            yp // TILE_SIZE)

    if pygame.key.get_pressed()[pygame.K_p]:
        print()
        print()
        print()
        print("BOARD")
        for i in board:
            print(*i)
    if pygame.key.get_pressed()[pygame.K_UP]:
        m.jump()
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        m.move('mr')
    elif pygame.key.get_pressed()[pygame.K_LEFT]:
        m.move('ml')
    else:
        m.move()

    screen.blit(background, (RES_X // 2 - int(m.x), RES_Y // 2 + 3 * TILE_SIZE - int(m.y)))
    f.draw()
    m.draw()
    #for x in foreground:
        #x.draw()
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
