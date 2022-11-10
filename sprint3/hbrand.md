# Sprint 3

Henry Brand - hbrandutk - PyTris

### What I planned to do
1. Shape Pack Module
2. Implement DAS
3. Fix the ghost piece

### What I did not do
I was able to fix some of the worst issues with the ghost piece and add color to it, but there were still some aspects I was unable to fix that will need to be fixed in the final sprint. It should be a fairly simple fix though.

### What problems you encountered
I had trouble with implementing the new shape pack module as many parts of pytris.py were hard coded to deal with seven pieces, so implementing new types of shapes meant those parts had to be discovered and debugged. 
DAS was successfully implemented but it revealed a new bug that was always present but previously unreachable. If the player uses DAS to get the piece outside of the board, the game will instantly crash. This might be harder to debug.
The cells on the board filled by the color of the ghost piece get treated as solid blocks by the clear_row function, this is a simple fix.

### Issues you worked on
I combined two of my tasks into one issue on github
[#1] https://github.com/utk-cs340-fall22/PyTris/issues/35	
[#2] https://github.com/utk-cs340-fall22/PyTris/issues/34

### Files you worked on
- pytris.py
- pytrisShapePacks.py
### What you accomplished
I succesfully implemented DAS, added coloring and fixed some issues with the ghost piece, and I added a new fun way to play the game with some shape pack templates that come included with the game.