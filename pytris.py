from operator import truediv
from unicodedata import name
import pygame
import random
import copy

pygame.font.init()

# Initialize music & sounds
volume = 0.1
pygame.mixer.init()
pygame.mixer.music.load('sounds/music.mp3')
pygame.mixer.music.set_volume(volume/2)

SERVER_IP = None
clear = pygame.mixer.Sound('sounds/clear.mp3')
tetris = pygame.mixer.Sound('sounds/tetris.mp3')
level_up = pygame.mixer.Sound('sounds/level_up.mp3')
game_over = pygame.mixer.Sound('sounds/game_over.mp3')

clear.set_volume(volume)
tetris.set_volume(volume)
level_up.set_volume(volume)
game_over.set_volume(volume)

# GLOBALS VARS
s_width = 1500
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
block_size = 30

top_left_x = 150 
top_left_y = (s_height - play_height) 
opponent_top_left_x = s_width - (top_left_x + play_width) - 200   # Opponent X position


# SHAPE FORMATS

S = [['.....',
      '.00..',
      '00...',
      '.....',
      '.....'],
     ['.....',
      '.0...',
      '.00..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.00..',
      '00...',
      '.....'],
     ['.....',
      '0....',
      '00...',
      '.0...',
      '.....']]

Z = [['.....',
      '00...',
      '.00..',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....'],
     ['.....',
      '.....',
      '00...',
      '.00...',
      '.....'],
     ['.....',
      '.0...',
      '00...',
      '0....',
      '.....']]

I = [['.....',
      '0000.',
      '.....',
      '.....',
      '.....'],
     ['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '0000.',
      '.....',
      '.....'],
     ['.0...',
      '.0...',
      '.0...',
      '.0...',
      '.....']]

O = [['.....',
      '.00..',
      '.00..',
      '.....',
      '.....']]

J = [['.....',
      '0....',
      '000..',
      '.....',
      '.....'],
     ['.....',
      '.00..',
      '.0...',
      '.0...',
      '.....'],
     ['.....',
      '.....',
      '000..',
      '..0..',
      '.....'],
     ['.....',
      '.0...',
      '.0...',
      '00...',
      '.....']]

L = [['.....',
      '..0..',
      '000..',
      '.....',
      '.....'],
     ['.....',
      '.0...',
      '.0...',
      '.00..',
      '.....'],
     ['.....',
      '.....',
      '000..',
      '0....',
      '.....'],
     ['.....',
      '00...',
      '.0...',
      '.0...',
      '.....']]

T = [['.....',
      '.0...',
      '000..',
      '.....',
      '.....'],
     ['.....',
      '.0...',
      '.00..',
      '.0...',
      '.....'],
     ['.....',
      '.....',
      '000..',
      '.0...',
      '.....'],
     ['.....',
      '.0...',
      '00...',
      '.0...',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (0, 0, 255), (255, 165, 0), (128, 0, 128)]
# index 0 - 6 represent shape

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
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

# Opponent Class for keeping track of the Opponent's board
# Currently a placeholder for later socket integration


class Opponent(object):
    def __init__(self, name, locked_pos={}):
        self.name = name
        self.locked_pos = locked_pos

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
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0) or grid[i][j] == (255, 255, 255)] for i in range(20)]
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
    shape_queue[:] = shapes[:]
    random.shuffle(shape_queue)
    for shape in shape_queue:
        bag_queue.append(Piece(5, 2, shape))
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


def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row and (255, 255, 255) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newkey = (x, y + inc)
                locked[newkey] = locked.pop(key)

    return inc


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


def draw_window(surface, grid, opponent_grid, opponent_name, score, line, level):
    surface.fill((0, 0, 0))

    #background image - 1500x700 atleast
    bg = pygame.image.load("backgrounds/bg1.jpg")
    surface.blit(bg,(0,0))

    font = pygame.font.SysFont('bauhaus93', 60)
    label = font.render('Player 1', 1, (255, 255, 255))
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

def call_server(server_ip,username,grid,opponent_grid,win):
    #print(grid)
    #print(opponent_grid)
    draw_window(win, grid, opponent_grid,"","","","",)
    return 0


# Add more settings in the future and allow for settings to be applied

def settings_menu(win):
    run = True

    vol_box = TextBox(600, 220, 400, 48)
    setting_boxes = [vol_box]

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

            for box in setting_boxes:
                box.handle(event)

        for box in setting_boxes:
            box.update()

        win.fill((0, 0, 0))

        font = pygame.font.Font(None, 110)
        label = font.render('Settings', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 25))

        label = FONT.render('Volume: ', True, (255, 255, 255))
        win.blit(label, (456, 227))

        font = pygame.font.Font(None, 28)
        label = font.render('Press ENTER to Apply', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 300))

        label = font.render('Press ESC to Return', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 330))

        label = font.render('Choose a background image', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 360))

        default_image_size = (100,100)
        default_y_pos = 420
        
        image2 = pygame.transform.scale(pygame.image.load('backgrounds/bg2.jpg'),default_image_size)
        win.blit(image2,(100,default_y_pos))

        image3 = pygame.transform.scale(pygame.image.load('backgrounds/bg3.jpg'),default_image_size)
        win.blit(image3,(300,default_y_pos))

        image4 = pygame.transform.scale(pygame.image.load('backgrounds/bg4.jpg'),default_image_size)
        win.blit(image4,(500,default_y_pos))

        image5 = pygame.transform.scale(pygame.image.load('backgrounds/bg5.jpg'),default_image_size)
        win.blit(image5,(700,default_y_pos))

        image6 = pygame.transform.scale(pygame.image.load('backgrounds/bg6.jpg'),default_image_size)
        win.blit(image6,(900,default_y_pos))

        image7 = pygame.transform.scale(pygame.image.load('backgrounds/bg7.jpg'),default_image_size)
        win.blit(image7,(1100,default_y_pos))

        image8 = pygame.transform.scale(pygame.image.load('background1.jpg'),default_image_size)
        win.blit(image8,(1300,default_y_pos))

        for box in setting_boxes:
            box.draw(win)

        pygame.display.flip()


def main(win,server_ip,username):
    locked_positions = {}
    grid = create_grid(locked_positions)
    bag_queue = create_queue() #Create a queue of seven pieces
    bag_queue.extend(create_queue()) #Append another seven pieces, now 14 pieces

    # Opponent Initialization
    opponent = Opponent("Player 2", locked_positions)
    opponent_grid = create_grid(opponent.locked_pos)

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
    das = 100

    pygame.mixer.music.play(-1)

    while run:
        grid = create_grid(locked_positions)
        opponent_grid = create_grid(opponent.locked_pos)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
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
            if event.type == pygame.QUIT:
                run = False
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
                if event.key == pygame.K_1:
                    create_garbage(grid, locked_positions, 1)
                if event.key == pygame.K_2:
                    create_garbage(grid, locked_positions, 2)
                if event.key == pygame.K_3:
                    create_garbage(grid, locked_positions, 3)
                if event.key == pygame.K_4:
                    create_garbage(grid, locked_positions, 4)
                if event.key == pygame.K_5:
                    create_garbage(grid, locked_positions, 5)
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.quit())

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # I went ahead and made the ghost piece but it's pretty buggy, fix it if you want Lohith
        # Make a deep copy of the current piece to use as the ghost
        # Move it below the current piece because it won't find any valid spaces otherwise
        # Recolor the cell to white
        ghost_shape_copy = copy.deepcopy(current_piece)
        while ghost_shape_copy.y < current_piece.y + 4 and ghost_shape_copy.y + 4 < 20:
            ghost_shape_copy.y += 4
        while valid_space(ghost_shape_copy, grid):
            ghost_shape_copy.y += 1
        ghost_shape_copy.y -= 1
        ghost_pos = convert_shape_format(ghost_shape_copy)
        for i in range(len(ghost_pos)):
            x, y = ghost_pos[i]
            if grid[y][x] == (0, 0, 0):
                grid[y][x] = (255, 255, 255)

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            if len(bag_queue) <= 7:
                bag_queue.extend(create_queue())
            current_piece = bag_queue.pop(0)
            if not valid_space(current_piece, grid):
                draw_text_middle(win, "YOU LOST!", 80, (255, 255, 255))
                pygame.mixer.Sound.play(game_over)
                pygame.mixer.music.stop()
                pygame.display.update()
                pygame.time.delay(1500)
                run = False
            hold_used = 0
            change_piece = False

            # update lines cleared
            cleared = clear_rows(grid, locked_positions)

            level_count += cleared
            line += cleared

            # update level & speed
            if cleared > 0 and level_count >= 10:
                level += 1
                leveled = True
                level_count -= 10
                fall_speed -= 0.025
                pygame.mixer.Sound.play(level_up)
                if fall_speed < 0.1: fall_speed = 0.1

            # update score
            if cleared == 1:
                score += 40 * (level + 1)
                if not leveled: pygame.mixer.Sound.play(clear)
            if cleared == 2:
                score += 100 * (level + 1)
                if not leveled: pygame.mixer.Sound.play(clear)
            if cleared == 3:
                score += 300 * (level + 1)
                if not leveled: pygame.mixer.Sound.play(clear)
            if cleared == 4:
                score += 1200 * (level + 1)
                if not leveled: pygame.mixer.Sound.play(tetris)

            leveled = False
        call_server(server_ip,username,grid,opponent_grid,win)

        draw_window(win, grid, opponent_grid, opponent.name, score, line, level)
        draw_queue(bag_queue, win, hold_piece)
        pygame.display.update()


def main_menu(win):
    run = True

    name_box = TextBox(600, 220, 400, 48)
    ip_box = TextBox(600, 280, 400, 48)
    text_boxes = [name_box, ip_box]

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:

                    name = name_box.get_text()
                    ip = ip_box.get_text()

                    if name != '' and ip != '':
                        print(f'Username -- { name }')
                        print(f'      IP -- { ip }')
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

        font = pygame.font.Font(None, 28)
        label = font.render('Press ENTER to Play', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 370))

        label = font.render('Press S for Settings', True, (255, 255, 255))
        win.blit(label, (750-(label.get_width()/2), 400))

        for box in text_boxes:
            box.draw(win)

        pygame.display.flip()

    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('PyTris')
main_menu(win)
