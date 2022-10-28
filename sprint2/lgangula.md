# Sprint 2

- Name: Lohith Gangula
- Github: LohithGangula
- Group: PyTris

### What you planned to do

- [#13](https://github.com/utk-cs340-fall22/PyTris/issues/13) Add hard drop
- [#14](https://github.com/utk-cs340-fall22/PyTris/issues/14) add ghost piece
- [#15](https://github.com/utk-cs340-fall22/PyTris/issues/15) Add backgrounds

### What you did not do

- I completed the hard drop and background selection for users, but not the ghost piece.

### What problems you encountered

- some problems with the background being consistently drawn. issue has to do with when the draw_window function is called. inconsistently works. 
- The ghost piece was pretty problematic, and even with Henry's help, it was not solved. Moving it to a future sprint

### Issues you worked on

- [#13](https://github.com/utk-cs340-fall22/PyTris/issues/13) Add hard drop
- [#15](https://github.com/utk-cs340-fall22/PyTris/issues/15) Add backgrounds to settings menu

### Files you worked on

- PyTris/pytris.py
- Pytris/backgrounds

### What you accomplished

During Sprint 2, I mostly focused on in game functionality and the settings users can change, specifically, backgrounds. I display a scaled down background in the settings page, and give the users options to pick from. once, the user picks a background (number keys) the background is changed when they start playing. I also added a hard drop so users can instantly place pieces using the space key. 