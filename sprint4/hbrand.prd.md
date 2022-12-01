# Product Requirements Document
Name: Henry Brand

Product Name: PyTris

## Background
There are plenty of open source Tetris clones on the market but enthusiasts have been looking for an open source clone with easy to host servers that is easy to mod with custom shapes and other modes. Branches of the project could potentially be monetized by selling modifications of the base game.

## Project Overview
PyTris is a client server application for the purpose of playing a multiplayer online Tetris game with friends. It allows for a one-on-one online match with user hosted servers as well as a singleplayer mode. 



## Features
Give at least 8 user stories to describe required features. These can come from the issues assigned to you during the 4 sprints, or you 
can create new items. Give a title or feature name for each story. Example: 
1. As a game developer, I wish to add my own modifications to the game through custom shape packs to enhance my gameplay experience.
2. As a player, I wish to be able to play alone and with friends.
3. When playing the game, as a gamer, I expect visual and audio quality sufficient enough to supplement the gameplay.
4. As a hosting company, I wish for my company to be able to easily host servers for a price that others can rent to play on.
5. As an experienced Tetris player, I wish for the game to have sufficient control options to suit my needs as a high level player.
6. As a user, I wish to be able to customize the looks of my game to suit my artistic style.
7. As a user with limited hardware availible, I hope that the game runs just as well on more limited hardware.
8. As a user of multiple computers with different operating systems, I wish that the game is bootable on several different platforms.

## Technologies to be used
The game will implement free Python tools, such as Pygame, to develop the client. Pygame is not sufficient for any game with large scale, but for a project of this scale it should be sufficient for what the game demands. The server side of the program will make use of websockets to communicate with clients to send and receive information about both players' boards.