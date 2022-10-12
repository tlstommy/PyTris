from operator import truediv
import pygame
import random

pygame.font.init()

# Initialize music & sounds
volume = 0.1
pygame.mixer.init()
pygame.mixer.music.load('sounds/music.mp3')
pygame.mixer.music.set_volume(volume/2)

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
opponent_top_left_x = s_width - (top_left_x + play_width)   # Opponent X position


# SHAPE FORMATS

S = [['.....',
      '..00.',
      '.00..',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.00..',
      '..00.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
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
      '.....']]

O = [['.....',
      '.00..',
      '.00..',
      '.....',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


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
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False

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
        bag_queue.append(Piece(5, 0, shape))
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


def clear_rows(grid, locked):

    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
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
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc


def draw_queue(queue, surface):
    font = pygame.font.SysFont('bauhaus93', 30)
    label = font.render('Queue', 1, (255,255,255))

    x = top_left_x + play_width + 50
    y = top_left_y + play_height/8

    for k in range(5):
        piece_format = queue[k].shape[queue[k].rotation % len(queue[k].shape)]
        for i, line in enumerate(piece_format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, queue[k].color, (x + j*block_size, (y + (75 * k)) + i*block_size, block_size, block_size), 0)

    surface.blit(label, (x + 10, y - 30))


def draw_window(surface, grid, opponent_grid, opponent_name, score, line, level):
    surface.fill((0, 0, 0))

    font = pygame.font.SysFont('bauhaus93', 60)
    label = font.render('Player 1', 1, (255, 255, 255))
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # Opponent Name
    label = font.render(opponent_name, 1, (255, 255, 255))
    surface.blit(label, (opponent_top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # display score
    font = pygame.font.SysFont('bauhaus93', 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 + 250
    surface.blit(label, (sx, sy))

    # display line
    label = font.render('Line: ' + str(line), 1, (255, 255, 255))
    sy -= 33
    surface.blit(label, (sx, sy))

    # display level
    label = font.render('Level: ' + str(level), 1, (255, 255, 255))
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


def main(win):
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
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.75
    level_count = 0
    level_time = 0
    leveled = False
    score = 0
    level = 0
    line = 0

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
                pygame.display.quit()

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
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.quit())

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            if len(bag_queue) <= 7:
                bag_queue.extend(create_queue())
            current_piece = bag_queue.pop(0)
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

        draw_window(win, grid, opponent_grid, opponent.name, score, line, level)
        draw_queue(bag_queue, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(win, "YOU LOST!", 80, (255,255,255))
            pygame.mixer.Sound.play(game_over)
            pygame.mixer.music.stop()
            pygame.display.update()
            pygame.time.delay(1500)
            run = False


# Future updates to this function:
# Add text-boxes for custom settings (DAS, ARR)
# Add a textbox for the IP address to connect to
# Pass these as arguments for the appropriate functions


def main_menu(win):
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle(win, 'Press Any Key To Play', 60, (255,255,255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('PyTris')
main_menu(win)