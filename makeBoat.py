import pygame, sys, sqlite3, math
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("boat make")

WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 255)
YELLOW = pygame.Color(255, 255, 0)
BLUE = pygame.Color(0, 0, 255)
BLACK = pygame.Color(0, 0, 0)

mousex, mousey = 0, 0

fontObj = pygame.font.Font('freesansbold.ttf', 30)
msg = "test"

index = 6
conn = sqlite3.connect("athletes.db")
c = conn.cursor()

grabbed = False
rowers = [[100, 90 + i*35, 15, RED, False] for i in range(8)]

def inCircle(x, y, cx, cy, r):
    return math.sqrt((x - cx)**2 + (y - cy)**2) <= r

while True:
    screen.fill(WHITE)

    pygame.draw.ellipse(screen, RED, (50, 50, 100, 350), 1)
    for i in rowers:
        pygame.draw.circle(screen, i[3], i[0:2], i[2])
        if i[4]:
            screen.blit(fontObj.render(str(i[4]), False, BLACK), (i[0]-i[2], i[1]-i[2], i[2], i[2]))
            
    pygame.draw.rect(screen, GREEN, (90, 360, 25, 25))

    for i in range(index - 5, index + 5):
        athlete = c.execute("SELECT * FROM athlete WHERE id = " + str(i) + ";").fetchone()
        msg = athlete[1] + u" " + athlete[2]
        msgSurf = fontObj.render(msg, False, BLACK)
        msgRect = msgSurf.get_rect()
        msgRect.topleft = (300, 25 + 40*(i - index + 5))
        screen.blit(msgSurf, msgRect)
        if i == index:
            pygame.draw.rect(screen, YELLOW, msgRect, 1)
            
    currentAthlete = c.execute("SELECT * FROM athlete WHERE id = " + str(index) + ";").fetchone()
    
    if grabbed:
        mousex, mousey = pygame.mouse.get_pos()
        pygame.draw.circle(screen, BLUE, (mousex, mousey), 15)

    for event in pygame.event.get():
        if event.type == QUIT:
            conn.commit()
            conn.close()
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_DOWN:
                index += 1
            elif event.key == K_UP:
                if index - 1 > 6:
                    index -= 1
            elif event.key == K_RETURN:
                grabbed = True
        elif event.type == MOUSEMOTION:
            if grabbed:
                mousex, mousey = event.pos
                for i in rowers:
                    if inCircle(mousex, mousey, i[0], i[1], i[2]):
                        pygame.draw.circle(screen, YELLOW, i[0:2], i[2], 1)
        elif event.type == MOUSEBUTTONUP:
            if grabbed:
                mousex, mousey = event.pos
                for i in rowers:
                    if inCircle(mousex, mousey, i[0], i[1], i[2]):
                        i[3] = BLUE
                        i[4] = currentAthlete[0]

    pygame.display.update()
    fpsClock.tick(30)
