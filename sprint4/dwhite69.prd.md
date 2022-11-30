# Product Requirements Document
Daniel White

Pytris

## Background
Pytris is a video game that uses elements from the original Tetris from the 1980's, but adds new elements to rejuvinate the old gameplay into a competitive player vs player experience. The old version of tetris is a single player game that is fairly simple, the user stacks blocks on top of each other, and clears full rows of blocks when completed. The goal of the original game is to survive as long as you can with oncoming blocks and increasing speed. In Pytris, it takes the same elements from tetris and uses a multiplayer experience turning tetris into a competitive game to see who can outlast the other.

## Project Overview
Pytris is a implementation of the prexisting tertris game in order to make the game more competitive with player vs player machanics. In addition to the online play, there are more elements added to tetris to give an edge to either player. These are elements such as instant drop, hold piece, and sending garbage to the other player. All these additions give an edge to which ever player can clear lines the fastest, and outlive their opponent.

## Features 
1. **Multiplayer Environment** As a competitive player, I want to be able to play tetris against other people
2. **Send Garbage** As a player, I want to be rewarded for clearing lines faster than my opponent, so I can win faster
3. **Ghost Piece** As a player, I want to be able to see where my piece will land on the board
4. **Hold Piece** As a player, I want to hold pieces that won't fit correctly for later, and use a different piece
5. **Username** As a player, I want to have a unique user name to identify myself as in online matches
6. **Opponent Board** As a player, I want to be able to view my opponent's progress of thier board to see if I am clost to winning
7. **Background** As a player, I want to see quality graphics with a nice backround image to ease my eyes from tetris.
8. **Music** As a player, I want music to serenate me as if I am stacking the blocks myself.

## Technologies to be used
Some of the main libraries include pygame, sockets, and JSON, which are used to run the game with different clients. Our project uses some prior implemetation of tetris using pygame from techwithtim. His documentation is found [Here](https://www.techwithtim.net/tutorials/game-development-with-python/tetris-pygame/tutorial-1/).