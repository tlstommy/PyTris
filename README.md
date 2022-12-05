# PyTris

PyTris is a client server application for the purpose of playing a multiplayer online Tetris game with friends. Players can connect to a server over a local network and play against eachother on a one-on-one battle. Players interact by clearing lines and sending "garbage lines" to the opponent with the purpose of topping their board out and winning the game. 

![alt text for screen readers](/cover.png "PyTris")

#  Contributors
* Henry Brand - [hbrand](https://github.com/hbrandutk)
* Thomas Smith - [lulamae12](https://github.com/lulamae12)
* Eli Kell - [eli-kell](https://github.com/eli-kell)
* Daniel White - [daniel-white99](https://github.com/daniel-white99)
* Lohith Gangula - [LohithGangula](https://github.com/LohithGangula)
# How to build
Python is needed to run PyTris, you can install Python here:
https://www.python.org/downloads/

Using PyTris is simple, to build simply clone the repository with 

```git clone https://github.com/utk-cs340-fall22/PyTris.git```


Install the required packages with 

```pip install -r requirements.txt```

And you're ready to run

# Starting a server for multiplayer
For demoing purposes, we have left all programs in PyTris as Python scripts instead of opting to create executables so that users on Linux, Windows, and OS X can run PyTris. To start a server, navigate to the PyTris directory and type

```py pytrisServer.py```, ```python pytrisServer.py```, or ```python3 pytrisServer.py``` 

depending on the version of Python installed.

After starting the server, a message showing your machine's local IP should print. PyTris only supports two player versus multiplayer over a local network at the moment, so you should be able to connect to the server on two different machines on the same network. Please be aware that this may not work on the UT network as UT's socket policy does not allow users to serve sockets externally on the eduroam or ut-open networks. 

To run the client, make sure you are still in the PyTris directory and type ```py pytris.py``` (or python, python3 depending on your version). The main menu should pop up with a settings menu and a place to type in a username and local IP to connect to. 

![alt text for screen readers](/example.png "PyTris")

For testing purposes, running two clients and connecting to a server on the same machine is the most reliable method. There is also the option to play singleplayer in the settings menu. When playing a singleplayer game, just type anything into the Server IP text box and click play to run.
# Gameplay
PyTris is old fashioned Tetris with a few modern twists that adhere to the modern Tetris™ guideline standards. Gameplay consists of clearing lines to send garbage lines to your opponent with the hope of those lines causing them to run out of space. Clearing a single line sends one garbage line, two sends two, and so on. The game ends when a player 

![alt text for screen readers](/gameplay.png "PyTris")
# Credits

Credit goes to Tim from https://www.techwithtim.net/
His tutorial was instrumental in figuring out how to get the basics of our own Tetris game running on Python.

# Licence
[LICENSE](https://github.com/utk-cs340-fall22/PyTris/blob/main/LICENSE)
