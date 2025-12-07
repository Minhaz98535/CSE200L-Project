import pygame as pg # type: ignore
pg.init()
info = pg.display.Info()

#Functions
def drawline():
    pg.draw.line(base, line, (200, 0), (200, 600), 6)
    pg.draw.line(base, line, (400, 0), (400, 600), 6)
    pg.draw.line(base, line, (0, 200), (600, 200), 6)
    pg.draw.line(base, line, (0, 400), (600, 400), 6)
    return

def addXO(pos_x, pos_y, move):
    if move == 1:
        img = x_img
    else:
        img = o_img

    if 0<=pos_x<=200:
        if 0<=pos_y<=200: width, height = 100, 100
        elif 201<=pos_y<=400: width, height = 100, 300
        elif 401<=pos_y<=600: width, height = 100, 500
    
    elif 201<=pos_x<=400:
        if 0<=pos_y<=200: width, height = 300, 100
        elif 201<=pos_y<=400: width, height = 300, 300
        elif 401<=pos_y<=600: width, height = 300, 500
    
    elif 401<=pos_x<=600:
        if 0<=pos_y<=200: width, height = 500, 100
        elif 201<=pos_y<=400: width, height = 500, 300
        elif 401<=pos_y<=600: width, height = 500, 500

    img_rect = img.get_rect(center = (width, height))
    base.blit(img, img_rect)

def update_board(board, pos_x, pos_y, move):
    if 0<=pos_x<=200:
        if 0<=pos_y<=200: x, y = 0, 0
        elif 201<=pos_y<=400: x, y = 1, 0
        elif 401<=pos_y<=600: x, y = 2, 0
    
    elif 201<=pos_x<=400:
        if 0<=pos_y<=200: x, y = 0, 1
        elif 201<=pos_y<=400: x, y = 1, 1
        elif 401<=pos_y<=600: x, y = 2, 1

    elif 401<=pos_x<=600:
        if 0<=pos_y<=200: x, y = 0, 2
        elif 201<=pos_y<=400: x, y = 1, 2
        elif 401<=pos_y<=600: x, y = 2, 2
    else:
        return

    if board[x][y] == None:
        board[x][y] = move
        addXO(pos_x, pos_y, move)
        return True

def isFilled(board):
    for i in board:
        for j in i:
            if j == None:
                return False    
    return True
        
def checkWinner(b):
    if b[0][0] == b[0][1] == b[0][2] != None:
        pg.draw.line(base, win_line, (0, 100), (600, 100), 10)
        return True
    if b[1][0] == b[1][1] == b[1][2] != None:
        pg.draw.line(base, win_line, (0, 300), (600, 300), 10)
        return True
    if b[2][0] == b[2][1] == b[2][2] != None:
        pg.draw.line(base, win_line, (0, 500), (600, 500), 10)
        return True
    if b[0][0] == b[1][0] == b[2][0] != None:
        pg.draw.line(base, win_line, (100, 0), (100, 600), 10)
        return True
    if b[0][1] == b[1][1] == b[2][1] != None:
        pg.draw.line(base, win_line, (300, 0), (300, 600), 10)
        return True
    if b[0][2] == b[1][2] == b[2][2] != None:
        pg.draw.line(base, win_line, (500, 0), (500, 600), 10)
        return True
    if b[0][0] == b[1][1] == b[2][2] != None:
        pg.draw.line(base, win_line, (0, 0), (600, 600), 10)
        return True
    if b[0][2] == b[1][1] == b[2][0] != None:
        pg.draw.line(base, win_line, (600, 0), (0, 600), 10)
        return True

def reset():
    global board, move, gameover
    for i in range(3):
        for j in range(3):
            board[i][j] = None
    
    move = 0
    gameover = False
    return True
    
def outro(move, x, o):
    x_rect = x_winner.get_rect(midbottom = (width//2, text_height_bottom))
    o_rect = o_winner.get_rect(midbottom = (width//2, text_height_bottom))
    if move == 1:
        screen.blit(x, x_rect)
    else:
        screen.blit(o, o_rect)

#Colors
board_color = (10, 10, 10)
line = "white"
win_line = (0, 255, 0, 15)

#Display
width, height = 600, 800
screen = pg.display.set_mode((width, height), pg.RESIZABLE)
screen.fill(board_color)
pg.display.set_caption("Tic Tac Toe!!")

#Board base
base = pg.Surface((600, 600))
bg = pg.image.load("assets/bg.jpg").convert_alpha()
bg = pg.transform.smoothscale(bg, (600, 600))
bg_rect = base.get_rect(center = (300, 300))
base.blit(bg, bg_rect)
drawline()

#Sounds
bg_sound = pg.mixer.Sound("assets/space.mp3")
bg_sound.set_volume(0.3)
click = pg.mixer.Sound("assets/click.mp3")
click.set_volume(0.1)
winner = pg.mixer.Sound("assets/winner.mp3")
bg_sound.play()

#Fonts and texts
text_font = pg.font.Font("assets/ScienceGothic.ttf", 50)
restart_font = pg.font.Font("assets/ScienceGothic.ttf", 30)

x_winner = text_font.render("X wins", True, "white")
o_winner = text_font.render("O wins", True, "white")

gameover_message = restart_font.render("CLICK ANYWHERE TO RESTART", False, "white")
draw_message = text_font.render("Match DRAWN!", False, "white")

#Images
x_img = pg.image.load("assets/cross.png").convert_alpha()
x_img = pg.transform.scale(x_img, (150, 150))

o_img = pg.image.load("assets/circle.png").convert_alpha()
o_img = pg.transform.smoothscale(o_img, (150, 150))


#Main Loop
board = [
    [None, None, None],
    [None, None, None],
    [None, None, None]
]

running = True
move = 1
restart = False
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.VIDEORESIZE:
            width, height = event.w, event.h
            screen = pg.display.set_mode((width, height), pg.RESIZABLE)
            screen.fill(board_color)
            
            
        if event.type == pg.MOUSEBUTTONDOWN:
            click.play()
            if restart:
                base.blit(bg, bg_rect)
                drawline()
                screen.fill(board_color)
                restart = False
            else:
                pos = pg.mouse.get_pos()
                x = pos[0] - base_rect.left
                y = pos[1] - base_rect.top
                updated = update_board(board, x, y, move)
                gameover = checkWinner(board)

                if updated:
                    if gameover:
                        outro(move, x_winner, o_winner)
                        winner.play()
                        screen.blit(gameover_message, gameover_message_rect)
                        restart = reset()
                        pg.display.update()
                    
                    elif isFilled(board):
                        screen.blit(draw_message, draw_text_rect)
                        winner.play()
                        screen.blit(gameover_message, gameover_message_rect)
                        restart = reset()
                        pg.display.update()
                    
                    if move == 1: move = 0
                    else: move = 1

    base_rect = base.get_rect(center = (width//2, height//2))
    gm_height_top = base_rect.bottom
    text_height_bottom = base_rect.top
    gameover_message_rect = gameover_message.get_rect(midtop = (width//2, gm_height_top))
    draw_text_rect = draw_message.get_rect(midbottom =(width//2, text_height_bottom))

    screen.blit(base, base_rect)
    pg.display.update()


