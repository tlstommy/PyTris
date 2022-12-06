import pygame,socket,sys,os,time
import random
#from pytrisServer import server
import json
import copy

from pytrisShapePacks import *
from pytrisClient import Client
from pytrisClient import PlayerInfo
from pytrisClient import Opponent

pygame.font.init()

EMPTY_GRID = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 
0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 
0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]

online = 1   # 1 for multiplayer; 0 for single-player

# Initialize music & sounds
music_volume = 0.1
pygame.mixer.init()
pygame.mixer.music.load('sounds/music.mp3')
pygame.mixer.music.set_volume(music_volume)

SERVER_IP = None
clear = pygame.mixer.Sound('sounds/clear.mp3')
tetris = pygame.mixer.Sound('sounds/tetris.mp3')
level_up = pygame.mixer.Sound('sounds/level_up.mp3')
game_over = pygame.mixer.Sound('sounds/game_over.mp3')

sfx_volume = 0.1
clear.set_volume(sfx_volume)
tetris.set_volume(sfx_volume)
level_up.set_volume(sfx_volume)
game_over.set_volume(sfx_volume)

# GLOBALS VARS
s_width = 1500
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
block_size = 30

top_left_x = 150 
top_left_y = (s_height - play_height) 
opponent_top_left_x = s_width - (top_left_x + play_width) - 200   # Opponent X position

shape_pack = SRS_PACK
DAS = 1000

COLOR_INACTIVE = pygame.Color(128, 128, 128)
COLOR_ACTIVE = pygame.Color(255, 255, 255)
FONT = pygame.font.Font(None, 48)


class TextBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False

            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(300, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_text(self):
        return self.text

    def get_state(self):
        return self.active


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_pack.shape_colors[shape_pack.shapes.index(shape)]
        self.ghost_color = shape_pack.ghost_colors[shape_pack.shapes.index(shape)]
        self.rotation = 0

# create_grid
#
# colors in the tetris play space by coloring in the 2D array by checking locked positions set to a given color
# locked position given in the format of {(x,y):(255,0,0)}


def create_grid(locked_pos={}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j,i)]
                grid[i][j] = c
    return grid

# convert_shape_format()
#
# Converts the easy-to-read shape arrays defined at the top of the program and returns a computer-friendly array
# Is used in valid_space to check whether the spot in grid[] and positions[] are both full
#
# param shape - the Piece object of the shape we are converting into the grid format
# return value - the converted position of the shape as a new position array which is relative to the game grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
    # The specifics of why this is done are confusing, watch part 2 at 4:30 for an explanation
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

# valid_space()
#
# Determines whether the shape is in a valid space or not (not occupied by another shape)
# Does this by iterating through the formatted array of the shape and comparing it to the grid - if the grid is colored
# then the spot is occupied
#
# param shape - the piece object being checked
# param grid - the grid array representing the current state of the board
# return value - boolean of if the position is valid


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0) or grid[i][j] in shape_pack.ghost_colors] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


# create_queue()
#
# Copies the global shapes list, shuffles the list, then creates another list of shape objects from that list and
# returns it
#
# return value - A list of seven randomly ordered shape objects


def create_queue():
    bag_queue = []
    shape_queue = []
    shape_queue[:] = shape_pack.shapes[:]
    random.shuffle(shape_queue)
    for shape in shape_queue:
        bag_queue.append(Piece(5, 3, shape))
    return bag_queue


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("bauhaus93", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))


def draw_grid(surface, grid, opponent_grid):
    sx = top_left_x
    sy = top_left_y
    rx = opponent_top_left_x

    # Player Grid
    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx+play_width-1, sy+ i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy),(sx + j*block_size, sy + play_height))
    
    # Opponent Grid
    for i in range(len(opponent_grid)):
        pygame.draw.line(surface, (128,128,128), (rx, sy + i*block_size), (rx+play_width-1, sy+ i*block_size))
        for j in range(len(opponent_grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (rx + j*block_size, sy), (rx + j*block_size, sy + play_height))

# create_garbage()
# Shifts all of the rows on the board in locked_positions up the number of garbage lines to be sent, then generates
# random garbage
# Meant to be called after receiving a lines cleared signal from the server
# grid - The 20x10 list containing tuples of the rgb color value of the cell
# locked - A dictionary keyed on grid coordinates with values a 3d tuple containing the color of the cell
# num_garbage - The number of lines to be created
def create_garbage(grid, locked, num_garbage):
    for key in sorted(list(locked), key=lambda x: x[1]):
        x, y = key
        newkey = (x, y - num_garbage)
        locked[newkey] = locked.pop(key)
    empty_row = random.randint(0, len(grid[0]) - 1)
    for i in range(num_garbage):
        for j in range(len(grid[0])):
            newkey = (j, (len(grid) - i) - 1)
            if j is not empty_row:
                locked[newkey] = (93, 93, 93)


def clear_lines(grid, locked):
    lines = 0

    for i in range(len(grid)):
        row = grid[i]
        count = 0
        for j in row:
            if j in all_colors or j == (93, 93, 93):
                count += 1

        if count == 10:
            ind = i
            lines += 1
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue

    if lines:
        yes = 0
        old_y = -1
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                if old_y == -1:
                    old_y = y

                if old_y != y:
                    yes += 1

                new_y = ind - yes

                newkey = (x, new_y)
                locked[newkey] = locked.pop(key)
                old_y = y

    return lines


def draw_queue(queue, surface, hold):
    font = pygame.font.SysFont('bauhaus93', 30)
    label = font.render('Queue', 1, (255,255,255))
    label2 = font.render('Hold', 1, (255, 255, 255))

    x = top_left_x + play_width + 50
    y = top_left_y + play_height/8

    for k in range(5):
        piece_format = queue[k].shape[queue[k].rotation % len(queue[k].shape)]
        for i, line in enumerate(piece_format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, queue[k].color, (x + j*block_size, (y + (75 * k)) + i*block_size, block_size, block_size), 0)

    if hold is not None:
        hold_piece_format = hold.shape[hold.rotation % len(hold.shape)]
        for i, line in enumerate(hold_piece_format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, hold.color, (top_left_x - 140 + (j * block_size), top_left_y + i * block_size + 75, block_size, block_size), 0)

    surface.blit(label, (x + 10, y - 30))
    surface.blit(label2, (top_left_x - 100, y - 30))


class background_image:
    def __init__(self,image_num=1):
        self._bg = pygame.image.load("backgrounds/bg"+str(image_num)+".jpg")
        self.num = image_num
    def get_background(self):
        return self._bg
    def set_background(self,image_num):
        self._bg = pygame.image.load("backgrounds/bg"+str(image_num)+".jpg")
        self.num = image_num
    def get_number(self):
        return self.num


bg = background_image()


def draw_window(surface, grid, opponent_grid, username, opponent_name, score, line, level):
    global bg

    surface.fill((0, 0, 0))

    #background image - 1500x700 atleast
    surface.blit(bg.get_background(),(0,0))

    font = pygame.font.SysFont('bauhaus93', 60)
    label = font.render(username, 1, (255, 255, 255))
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # Opponent Name
    label = font.render(opponent_name, 1, (255, 255, 255))
    surface.blit(label, (opponent_top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # display score
    font = pygame.font.SysFont('bauhaus93', 30)
    label = font.render(f'Score: { score }', True, (255, 255, 255))
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 + 250
    surface.blit(label, (sx, sy))

    # display line
    label = font.render(f'Line: { line }', True, (255, 255, 255))
    sy -= 33
    surface.blit(label, (sx, sy))

    # display level
    label = font.render(f'Level: { level }', True, (255, 255, 255))
    sy -= 33
    surface.blit(label, (sx, sy))

    # Opponent score
    label = font.render(f'Score: 0', True, (255, 255, 255))
    sx = opponent_top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 + 250
    surface.blit(label, (sx, sy))

    # Opponent line
    label = font.render(f'Line: 0', True, (255, 255, 255))
    sy -= 33
    surface.blit(label, (sx, sy))

    # Opponent level
    label = font.render(f'Level: 0', True, (255, 255, 255))
    sy -= 33
    surface.blit(label, (sx, sy))

    # Player Grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (128, 128, 128), (top_left_x, top_left_y, play_width, play_height), 5)
    
    # Opponent Grid
    for i in range(len(opponent_grid)):
        for j in range(len(opponent_grid[i])):
            pygame.draw.rect(surface, opponent_grid[i][j], (opponent_top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)
    
    pygame.draw.rect(surface, (128, 128, 128), (opponent_top_left_x, top_left_y, play_width, play_height), 5)
    draw_grid(surface, grid, opponent_grid)

def call_server(server_ip,localIP,username,grid,opponent_grid,win,client,signalType, game_end, send_garbage):
    #print(grid)
    jsonData = {
                "username":username, 
                "ip":localIP,
                "recvPort":25000,
                "signalType":signalType,
                "currentGrid":grid,
                "game_end":game_end,
                "send_garbage":send_garbage,
                }

    client.createClientSocket();client.sendData(jsonData)
    
    try:
        opponent = client.receiveData()
    except:
        opponent = {}

    
    return opponent


def settings_menu(win):
    run = True

    esc = pygame.Rect(5, 5, 40, 40)
    packs = pygame.Rect(625, 190, 250, 48)
    sounds = pygame.Rect(625, 240, 250, 48)
    network = pygame.Rect(625, 290, 250, 48)
    controls = pygame.Rect(625, 340, 250, 48)
    backgrounds = pygame.Rect(625, 390, 250, 48)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if esc.collidepoint(event.pos):
                    run = False
                if packs.collidepoint(event.pos):
                    pack_menu(win)
                if sounds.collidepoint(event.pos):
                    sound_menu(win)
                if network.collidepoint(event.pos):
                    network_menu(win)
                if controls.collidepoint(event.pos):
                    control_menu(win)
                if backgrounds.collidepoint(event.pos):
                    background_menu(win)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_p:
                    pack_menu(win)
                if event.key == pygame.K_s:
                    sound_menu(win)
                if event.key == pygame.K_n:
                    network_menu(win)
                if event.key == pygame.K_c:
                    control_menu(win)
                if event.key == pygame.K_b:
                    background_menu(win)

        win.fill((0, 0, 0))

        font = pygame.font.Font(None, 110)
        label = font.render('Settings', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 25))

        label = FONT.render('Packs', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 200))

        label = FONT.render('Sounds', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 250))

        label = FONT.render('Network', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 300))

        label = FONT.render('Controls', True, (255, 255, 255))
        win.blit(label, (750 - (label.get_width() / 2), 350))

        label = FONT.render('Backgrounds', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 400))

        label = FONT.render('X', True, (255, 255, 255))
        win.blit(label, (14, 10))

        pygame.draw.rect(win, (50, 50, 50), esc, 2)
        pygame.draw.rect(win, (50, 50, 50), packs, 2)
        pygame.draw.rect(win, (50, 50, 50), sounds, 2)
        pygame.draw.rect(win, (50, 50, 50), network, 2)
        pygame.draw.rect(win, (50, 50, 50), controls, 2)
        pygame.draw.rect(win, (50, 50, 50), backgrounds, 2)

        pygame.display.flip()


def pack_menu(win):
    run = True
    global shape_pack

    esc = pygame.Rect(5, 5, 40, 40)
    srs = pygame.Rect(625, 215, 250, 48)
    mono = pygame.Rect(625, 265, 250, 48)
    domino = pygame.Rect(625, 315, 250, 48)
    triomino = pygame.Rect(625, 365, 250, 48)
    everything = pygame.Rect(625, 415, 250, 48)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if esc.collidepoint(event.pos):
                    run = False
                if srs.collidepoint(event.pos):
                    shape_pack = SRS_PACK
                if mono.collidepoint(event.pos):
                    shape_pack = MONOMINO_PACK
                if domino.collidepoint(event.pos):
                    shape_pack = DOMINO_PACK
                if triomino.collidepoint(event.pos):
                    shape_pack = TRIOMINO_PACK
                if everything.collidepoint(event.pos):
                    shape_pack = EVERYTHING_PACK

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    shape_pack = SRS_PACK
                if event.key == pygame.K_2:
                    shape_pack = MONOMINO_PACK
                if event.key == pygame.K_3:
                    shape_pack = DOMINO_PACK
                if event.key == pygame.K_4:
                    shape_pack = TRIOMINO_PACK
                if event.key == pygame.K_5:
                    shape_pack = EVERYTHING_PACK
                if event.key == pygame.K_ESCAPE:
                    run = False

        win.fill((0, 0, 0))

        font = pygame.font.Font(None, 110)
        label = font.render('Packs', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 25))

        font = pygame.font.Font(None, 28)
        label = font.render(f'Current Pack: { shape_pack.name }', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 150))

        label = FONT.render('SRS', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 225))

        label = FONT.render('Monominos', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 275))

        label = FONT.render('Dominos', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 325))

        label = FONT.render('Triominos', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 375))

        label = FONT.render('Everything', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 425))

        label = FONT.render('X', True, (255, 255, 255))
        win.blit(label, (14, 10))

        pygame.draw.rect(win, (50, 50, 50), esc, 2)
        pygame.draw.rect(win, (50, 50, 50), srs, 2)
        pygame.draw.rect(win, (50, 50, 50), mono, 2)
        pygame.draw.rect(win, (50, 50, 50), domino, 2)
        pygame.draw.rect(win, (50, 50, 50), triomino, 2)
        pygame.draw.rect(win, (50, 50, 50), everything, 2)

        pygame.display.flip()


def sound_menu(win):
    run = True
    global music_volume, sfx_volume

    music_box = TextBox(600, 220, 400, 48)
    sfx_box = TextBox(600, 280, 400, 48)
    text_boxes = [music_box, sfx_box]

    esc = pygame.Rect(5, 5, 40, 40)
    apply = pygame.Rect(650, 363, 200, 48)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if esc.collidepoint(event.pos):
                    run = False
                if apply.collidepoint(event.pos):
                    music = music_box.get_text()
                    sfx = sfx_box.get_text()

                    if music != '':
                        music_volume = float(music)

                        if music_volume < 0:
                            music_volume = 0
                        if music_volume > 1:
                            music_volume = 1

                        pygame.mixer.music.set_volume(music_volume)

                    if sfx != '':
                        sfx_volume = float(sfx)

                        if sfx_volume < 0:
                            sfx_volume = 0
                        if sfx_volume > 1:
                            sfx_volume = 1

                        clear.set_volume(sfx_volume)
                        tetris.set_volume(sfx_volume)
                        level_up.set_volume(sfx_volume)
                        game_over.set_volume(sfx_volume)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    music = music_box.get_text()
                    sfx = sfx_box.get_text()

                    if music != '':
                        music_volume = float(music)

                        if music_volume < 0:
                            music_volume = 0
                        if music_volume > 1:
                            music_volume = 1

                        pygame.mixer.music.set_volume(music_volume)

                    if sfx != '':
                        sfx_volume = float(sfx)

                        if sfx_volume < 0:
                            sfx_volume = 0
                        if sfx_volume > 1:
                            sfx_volume = 1

                        clear.set_volume(sfx_volume)
                        tetris.set_volume(sfx_volume)
                        level_up.set_volume(sfx_volume)
                        game_over.set_volume(sfx_volume)

                if event.key == pygame.K_ESCAPE:
                    run = False

            for box in text_boxes:
                box.handle(event)

        for box in text_boxes:
            box.update()

        win.fill((0, 0, 0))

        font = pygame.font.Font(None, 110)
        label = font.render('Sounds', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 25))

        font = pygame.font.Font(None, 28)
        label = font.render(f'Music Volume: { music_volume }', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 150))

        label = font.render(f'SFX Volume: { sfx_volume }', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 175))

        label = FONT.render('Music Volume: ', True, (255, 255, 255))
        win.blit(label, (350, 227))

        label = FONT.render('SFX Volume: ', True, (255, 255, 255))
        win.blit(label, (380, 287))

        label = FONT.render('Apply', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 370))

        label = FONT.render('X', True, (255, 255, 255))
        win.blit(label, (14, 10))

        pygame.draw.rect(win, (50, 50, 50), esc, 2)
        pygame.draw.rect(win, (50, 50, 50), apply, 2)

        for box in text_boxes:
            box.draw(win)

        pygame.display.flip()


def network_menu(win):
    run = True
    global online

    esc = pygame.Rect(5, 5, 40, 40)
    multi = pygame.Rect(625, 218, 250, 48)
    single = pygame.Rect(625, 268, 250, 48)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if esc.collidepoint(event.pos):
                    run = False
                if multi.collidepoint(event.pos):
                    online = 1
                if single.collidepoint(event.pos):
                    online = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    online = 1
                if event.key == pygame.K_2:
                    online = 0
                if event.key == pygame.K_ESCAPE:
                    run = False

        win.fill((0, 0, 0))

        font = pygame.font.Font(None, 110)
        label = font.render('Network', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 25))

        font = pygame.font.Font(None, 28)

        if online:
            label = font.render('Mode: Multiplayer', True, (255, 255, 255))
        else:
            label = font.render('Mode: Singleplayer', True, (255, 255, 255))

        win.blit(label, (750-(label.get_width()/2), 150))

        label = FONT.render('Multiplayer', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 225))

        label = FONT.render('Singleplayer', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 275))

        label = FONT.render('X', True, (255, 255, 255))
        win.blit(label, (14, 10))

        pygame.draw.rect(win, (50, 50, 50), esc, 2)
        pygame.draw.rect(win, (50, 50, 50), multi, 2)
        pygame.draw.rect(win, (50, 50, 50), single, 2)

        pygame.display.flip()


def control_menu(win):
    run = True
    global DAS

    das_box = TextBox(600, 220, 400, 48)
    text_boxes = [das_box]

    esc = pygame.Rect(5, 5, 40, 40)
    apply = pygame.Rect(650, 297, 200, 48)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if esc.collidepoint(event.pos):
                    run = False
                if apply.collidepoint(event.pos):
                    das = das_box.get_text()

                    if das != '':
                        DAS = int(das)

                        if DAS < 0:
                            DAS = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    das = das_box.get_text()

                    if das != '':
                        DAS = int(das)

                        if DAS < 0:
                            DAS = 0

                if event.key == pygame.K_ESCAPE:
                    run = False

            for box in text_boxes:
                box.handle(event)

        for box in text_boxes:
            box.update()

        win.fill((0, 0, 0))

        font = pygame.font.Font(None, 110)
        label = font.render('Controls', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 25))

        font = pygame.font.Font(None, 28)
        label = font.render(f'DAS: { DAS }', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 150))

        label = FONT.render('DAS: ', True, (255, 255, 255))
        win.blit(label, (500, 227))

        label = FONT.render('Apply', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 304))

        label = FONT.render('X', True, (255, 255, 255))
        win.blit(label, (14, 10))

        pygame.draw.rect(win, (50, 50, 50), esc, 2)
        pygame.draw.rect(win, (50, 50, 50), apply, 2)

        for box in text_boxes:
            box.draw(win)

        pygame.display.flip()


def background_menu(win):
    run = True
    global bg

    esc = pygame.Rect(5, 5, 40, 40)
    bg_1 = pygame.Rect(75, 225, 150, 150)
    bg_2 = pygame.Rect(275, 225, 150, 150)
    bg_3 = pygame.Rect(475, 225, 150, 150)
    bg_4 = pygame.Rect(675, 225, 150, 150)
    bg_5 = pygame.Rect(875, 225, 150, 150)
    bg_6 = pygame.Rect(1075, 225, 150, 150)
    bg_7 = pygame.Rect(1275, 225, 150, 150)


    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if esc.collidepoint(event.pos):
                    run = False
                if bg_1.collidepoint(event.pos):
                    bg.set_background(1)
                if bg_2.collidepoint(event.pos):
                    bg.set_background(2)
                if bg_3.collidepoint(event.pos):
                    bg.set_background(3)
                if bg_4.collidepoint(event.pos):
                    bg.set_background(4)
                if bg_5.collidepoint(event.pos):
                    bg.set_background(5)
                if bg_6.collidepoint(event.pos):
                    bg.set_background(6)
                if bg_7.collidepoint(event.pos):
                    bg.set_background(7)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    bg.set_background(1)
                if event.key == pygame.K_2:
                    bg.set_background(2)
                if event.key == pygame.K_3:
                    bg.set_background(3)
                if event.key == pygame.K_4:
                    bg.set_background(4)
                if event.key == pygame.K_5:
                    bg.set_background(5)
                if event.key == pygame.K_6:
                    bg.set_background(6)
                if event.key == pygame.K_7:
                    bg.set_background(7)
                if event.key == pygame.K_ESCAPE:
                    run = False

        win.fill((0, 0, 0))

        font = pygame.font.Font(None, 110)
        label = font.render('Backgrounds', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 25))

        font = pygame.font.Font(None, 28)
        label = font.render(f'Current Background: { bg.get_number() }', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 150))

        default_image_size = (100, 100)
        default_y_pos = 250

        label = font.render('1', True, (255, 255, 255))
        win.blit(label, (150, default_y_pos + 150))
        image8 = pygame.transform.scale(pygame.image.load('backgrounds/bg1.jpg'), default_image_size)
        win.blit(image8, (100, default_y_pos))

        font = pygame.font.Font(None, 28)
        label = font.render('2', True, (255, 255, 255))
        win.blit(label, (350, default_y_pos + 150))
        image2 = pygame.transform.scale(pygame.image.load('backgrounds/bg2.jpg'), default_image_size)
        win.blit(image2, (300, default_y_pos))

        label = font.render('3', True, (255, 255, 255))
        win.blit(label, (550, default_y_pos + 150))
        image3 = pygame.transform.scale(pygame.image.load('backgrounds/bg3.jpg'), default_image_size)
        win.blit(image3, (500, default_y_pos))

        label = font.render('4', True, (255, 255, 255))
        win.blit(label, (750, default_y_pos + 150))
        image4 = pygame.transform.scale(pygame.image.load('backgrounds/bg4.jpg'), default_image_size)
        win.blit(image4, (700, default_y_pos))

        label = font.render('5', True, (255, 255, 255))
        win.blit(label, (950, default_y_pos + 150))
        image5 = pygame.transform.scale(pygame.image.load('backgrounds/bg5.jpg'), default_image_size)
        win.blit(image5, (900, default_y_pos))

        label = font.render('6', True, (255, 255, 255))
        win.blit(label, (1150, default_y_pos + 150))
        image6 = pygame.transform.scale(pygame.image.load('backgrounds/bg6.jpg'), default_image_size)
        win.blit(image6, (1100, default_y_pos))

        label = font.render('7', True, (255, 255, 255))
        win.blit(label, (1350, default_y_pos + 150))
        image7 = pygame.transform.scale(pygame.image.load('backgrounds/bg7.jpg'), default_image_size)
        win.blit(image7, (1300, default_y_pos))

        label = FONT.render('X', True, (255, 255, 255))
        win.blit(label, (14, 10))

        pygame.draw.rect(win, (50, 50, 50), esc, 2)
        pygame.draw.rect(win, (50, 50, 50), bg_1, 2)
        pygame.draw.rect(win, (50, 50, 50), bg_2, 2)
        pygame.draw.rect(win, (50, 50, 50), bg_3, 2)
        pygame.draw.rect(win, (50, 50, 50), bg_4, 2)
        pygame.draw.rect(win, (50, 50, 50), bg_5, 2)
        pygame.draw.rect(win, (50, 50, 50), bg_6, 2)
        pygame.draw.rect(win, (50, 50, 50), bg_7, 2)

        pygame.display.flip()


def wait_screen(win):

    win.fill((0, 0, 0))

    font = pygame.font.Font(None, 125)
    label = font.render('Connecting...', True, (255, 255, 255))
    win.blit(label, (750-(label.get_width()/2), 350-(label.get_height()/2)))

    pygame.display.flip()


def main(win,server_ip,username):
    locked_positions = {}
    grid = create_grid(locked_positions)
    bag_queue = create_queue()
    while len(bag_queue) <= 7:
        bag_queue.extend(create_queue())

    #server stuff
    if online == 1:
        client = Client(server_ip,8888,recvPort=25000)
        localIP =socket.gethostbyname(socket.gethostname())



    # Opponent Initialization
    opponent = Opponent("Player 2", locked_positions)
    opponent_grid = create_grid(opponent.locked_pos)
    total_left_held = 0
    total_right_held = 0
    change_piece = False
    run = True
    current_piece = bag_queue.pop(0)
    hold_piece = None
    hold_used = 0
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.75
    level_count = 0
    level_time = 0
    leveled = False
    score = 0
    level = 0
    line = 0
    garbage_queue = 0
    game_end = False

    if online == 1:
        opponent_info = call_server(server_ip, localIP, username, grid, opponent_grid, win, client, "standard", game_end, 0)
        while len(opponent_info) == 0:
            opponent_info = call_server(server_ip, localIP, username, grid, opponent_grid, win, client, "standard", game_end, 0)

    pygame.mixer.music.play(-1)
    if online == 1:
        opponent.name = opponent_info["username"]

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        cleared = 0
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if online == 1:
                if opponent_info["game_end"] == True:
                    draw_text_middle(win, "YOU WON!", 80, (255, 255, 255))
                    pygame.mixer.Sound.play(game_over)
                    pygame.mixer.music.stop()
                    pygame.display.update()
                    pygame.time.delay(1500)
                    run = False

            if event.type == pygame.QUIT:
                run = False
                game_end = True
                if online == 1:
                    opponent_info = call_server(server_ip, localIP, username, grid, opponent_grid, win, client, "standard", game_end, cleared)
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
                if event.key == pygame.K_z:
                    current_piece.rotation -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation += 1
                if event.key == pygame.K_a:
                    current_piece.rotation += 2
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 2
                if event.key == pygame.K_LSHIFT and hold_used == 0:
                    current_piece.x = 5
                    current_piece.y = 2
                    current_piece.rotation = 0
                    if hold_piece is None:
                        hold_piece = current_piece
                        current_piece = bag_queue.pop(0)
                    else:
                        temp_piece = hold_piece
                        hold_piece = current_piece
                        current_piece = temp_piece
                    hold_used = 1
                if event.key == pygame.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    change_piece = 1
                if event.key == pygame.K_ESCAPE:
                    # send info over server
                    if online:
                        game_end = True
                        opponent_info = call_server(server_ip, localIP, username, grid, opponent_grid, win, client, "standard", game_end, cleared)
                        exit()
                    else:
                        run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            total_left_held += clock.get_rawtime()
            if total_left_held >= DAS:
                while valid_space(current_piece, grid):
                    current_piece.x -= 1
                current_piece.x += 1
        else:
            total_left_held = 0

        if keys[pygame.K_RIGHT]:
            total_right_held += clock.get_rawtime()
            if total_right_held >= DAS:
                while valid_space(current_piece, grid):
                    current_piece.x += 1
                current_piece.x -= 1
        else:
            total_right_held = 0

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        ghost_shape_copy = copy.deepcopy(current_piece)
        while ghost_shape_copy.y < current_piece.y + 4 and ghost_shape_copy.y < 20:
            ghost_shape_copy.y += 1
        while valid_space(ghost_shape_copy, grid):
            ghost_shape_copy.y += 1
        ghost_shape_copy.y -= 1
        ghost_pos = convert_shape_format(ghost_shape_copy)
        for i in range(len(ghost_pos)):
            x, y = ghost_pos[i]
            if grid[y][x] == (0, 0, 0):
                grid[y][x] = ghost_shape_copy.ghost_color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            while len(bag_queue) <= 7:
                bag_queue.extend(create_queue())
            current_piece = bag_queue.pop(0)
            if not valid_space(current_piece, grid):
                draw_text_middle(win, "YOU LOST!", 80, (255, 255, 255))
                game_end = True
                pygame.mixer.Sound.play(game_over)
                pygame.mixer.music.stop()
                pygame.display.update()
                pygame.time.delay(1500)
                run = False
            hold_used = 0
            change_piece = False

            # update lines cleared
            cleared = clear_lines(grid, locked_positions)

            level_count += cleared
            line += cleared

            # update level & speed
            if cleared > 0 and level_count >= 10:
                level += 1
                leveled = True
                level_count -= 10
                fall_speed -= 0.025
                pygame.mixer.Sound.play(level_up)
                if fall_speed < 0.1:
                    fall_speed = 0.1

            # update score
            if cleared == 1:
                score += 40 * (level + 1)
                if not leveled:
                    pygame.mixer.Sound.play(clear)
            if cleared == 2:
                score += 100 * (level + 1)
                # send 1 line
                if not leveled:
                    pygame.mixer.Sound.play(clear)
            if cleared == 3:
                score += 300 * (level + 1)
                # send 2 lines
                if not leveled:
                    pygame.mixer.Sound.play(clear)
            if cleared == 4:
                score += 1200 * (level + 1)
                # send 3 lines
                if not leveled:
                    pygame.mixer.Sound.play(tetris)

            leveled = False
            if garbage_queue > 0:
                create_garbage(grid, locked_positions, garbage_queue)
                garbage_queue = 0


        if online == 1:
            try:
                opponent_info = call_server(server_ip, localIP, username, grid, opponent_grid, win, client, "standard", game_end, cleared)

            except TypeError as e:
                print("ERROR:", e)

            opponent_grid = opponent_info["currentGrid"]
            garbage_queue += opponent_info["send_garbage"]
        draw_window(win, grid, opponent_grid, username, opponent.name, score, line, level)
        draw_queue(bag_queue, win, hold_piece)


        pygame.display.update()


def main_menu(win):
    run = True

    name_box = TextBox(600, 220, 400, 48)
    ip_box = TextBox(600, 280, 400, 48)
    text_boxes = [name_box, ip_box]

    esc = pygame.Rect(5, 5, 40, 40)
    play = pygame.Rect(675, 368, 150, 48)
    settings = pygame.Rect(650, 593, 200, 48)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if esc.collidepoint(event.pos):
                    run = False

                if play.collidepoint(event.pos):
                    name = name_box.get_text()
                    ip = ip_box.get_text()

                    if name != '' and ip != '':
                        print(f'Username -- { name }')
                        print(f'      IP -- { ip }')

                        wait_screen(win)
                        main(win, ip, name)

                if settings.collidepoint(event.pos):
                    settings_menu(win)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:

                    name = name_box.get_text()
                    ip = ip_box.get_text()

                    #print("ipdebug on!")
                    #ip = "216.96.223.241"

                    if name != '' and ip != '':
                        print(f'Username -- { name }')
                        print(f'      IP -- { ip }')
                        #create a new client for the server at serverIP:8888, and open on port 25000 for reciveing

                        wait_screen(win)
                        main(win, ip, name)

                active = False

                for box in text_boxes:
                    active = active or box.get_state()

                if event.key == pygame.K_s and not active:
                    settings_menu(win)

            for box in text_boxes:
                box.handle(event)

        for box in text_boxes:
            box.update()

        win.fill((0, 0, 0))

        font = pygame.font.Font(None, 125)
        label = font.render('PyTris', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 75))

        label = FONT.render('Username: ', True, (255, 255, 255))
        win.blit(label, (410, 227))

        label = FONT.render('Server IP: ', True, (255, 255, 255))
        win.blit(label, (428, 287))

        label = FONT.render('X', True, (255, 255, 255))
        win.blit(label, (14, 10))

        label = FONT.render('Play', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 375))

        label = FONT.render('Settings', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 600))

        pygame.draw.rect(win, (50, 50, 50), esc, 2)
        pygame.draw.rect(win, (50, 50, 50), play, 2)
        pygame.draw.rect(win, (50, 50, 50), settings, 2)

        for box in text_boxes:
            box.draw(win)

        pygame.display.flip()

    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('PyTris')
main_menu(win)
