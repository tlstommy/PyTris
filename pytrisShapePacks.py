class ShapePack:
    def __init__(self, name, shapes, colors, ghost_colors):
        self.name = name
        self.shapes = shapes
        self.shape_colors = colors
        self.ghost_colors = ghost_colors


# SRS ROTATION SYSTEM - All Tetrominos with the super rotation system
srs_S = [['.....',
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

srs_Z = [['.....',
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

srs_I = [['.....',
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

srs_O = [['.....',
          '.00..',
          '.00..',
          '.....',
          '.....']]

srs_J = [['.....',
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

srs_L = [['.....',
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

srs_T = [['.....',
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

srs_shapes = [srs_S, srs_Z, srs_I, srs_O, srs_J, srs_L, srs_T]
srs_shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (0, 0, 255), (255, 165, 0), (165, 0, 165)]
srs_ghost_colors = [(0, 128, 0), (128, 0, 0), (0, 128, 128), (128, 128, 0), (0, 0, 128), (128, 85, 0), (82, 0, 82)]

# MONOMINOS - All blocks consisting of one mino
monomino = [['.....',
             '.0...',
             '.....',
             '.....',
             '.....'],
            ['.....',
             '.....',
             '.0...',
             '.....',
             '.....']]
monomino_shapes = [monomino]
monomino_colors = [(0, 255, 255)]
monomino_ghost_colors = [(0, 128, 128)]

# DOMINOS - All blocks consisting of two minos
domino = [['.....',
           '.00..',
           '.....',
           '.....',
           '.....'],
          ['.....',
           '..0..',
           '..0..',
           '.....',
           '.....']]

domino_shapes = [domino]
domino_colors = [(255, 0, 0)]
domino_ghost_colors = [(128, 0, 0)]


# TRIOMINOS - All blocks consisting of 3 minos
triomino_I =[['.....',
              '.000.',
              '.....',
              '.....',
              '.....'],
             ['..0..',
              '..0..',
              '..0..',
              '.....',
              '.....'],
             ['.....',
              '.....',
              '.000.',
              '.....',
              '.....'],
             ['.0...',
              '.0...',
              '.0...',
              '.....',
              '.....']]

triomino_V = [['.....',
               '.0...',
               '.00..',
               '.....',
               '.....'],
              ['.....',
               '.....',
               '.00..',
               '.0...',
               '.....'],
              ['.....',
               '.....',
               '00...',
               '.0...',
               '.....'],
              ['.....',
               '.0...',
               '00...',
               '.....',
               '.....']]

triomino_shapes = [triomino_I, triomino_V]
triomino_colors = [(0, 255, 255), (165, 0, 165)]
triomino_ghost_colors = [(0, 128, 128), (82, 0, 82)]

all_shapes = [srs_S, srs_Z, srs_I, srs_O, srs_J, srs_L, srs_T, monomino, domino, triomino_I, triomino_V]
all_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (0, 0, 255), (255, 165, 0), (165, 0, 165), (0, 255, 255), (255, 0, 0), (0, 255, 255), (165, 0, 165)]
all_ghost_colors = [(0, 128, 0), (128, 0, 0), (0, 128, 128), (128, 128, 0), (0, 0, 128), (128, 85, 0), (82, 0, 82), (0, 128, 128), (128, 0, 0), (0, 128, 128), (82, 0, 82)]

SRS_PACK = ShapePack("SRS", srs_shapes, srs_shape_colors, srs_ghost_colors)
MONOMINO_PACK = ShapePack("Monominos", monomino_shapes, monomino_colors, monomino_ghost_colors)
DOMINO_PACK = ShapePack("Dominos", domino_shapes, domino_colors, domino_ghost_colors)
TRIOMINO_PACK = ShapePack("Triominos", triomino_shapes, triomino_colors, triomino_ghost_colors)
EVERYTHING_PACK = ShapePack("Everything", all_shapes, all_colors, all_ghost_colors)

shape_packs = [SRS_PACK, MONOMINO_PACK, DOMINO_PACK, TRIOMINO_PACK, EVERYTHING_PACK]