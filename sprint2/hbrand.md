# Sprint 2

Henry Brand - hbrandutk - PyTris

### What I planned to do
1. Garbage Creation Function
2. SRS Pieces
3. DAS/ARR
4. Ghost piece

### What I did not do
I was unable to finish DAS/ARR

### What problems you encountered
Getting the amount of time a key has been held caused me issues in the main game loop, so I was not able to determine when I should auto shift a piece to the left or right
There were problems with my code after I merged with Dan and Eli's latest changes, but my code works on its own. The issues are likely caused by changes made to the locked_pieces dict

### Issues you worked on
[#1] https://github.com/utk-cs340-fall22/PyTris/issues/23
[#2] https://github.com/utk-cs340-fall22/PyTris/issues/20
[#3] https://github.com/utk-cs340-fall22/PyTris/issues/18

### Files you worked on
- pytris.py
### What you accomplished
I added the functionality of a ghost piece to guide the player below the current piece before it has been placed.
I added a create_garbage function to create some garbage lines on the board. This function will be called in the fincal product when the server sends a message that lines have been cleared
I made the game abide more closely by modern tetris guidelines by having the pieces rotate in the correct way