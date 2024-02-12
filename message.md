# Street Simulation

This repo contains the **street simulation project** of @freely1967, @QuantumVortex1 and @Kikiiii2004.
## What is this?
This project originates from the Programming course. Our proficiency in Python, our teamwork skills, and our talent in using GitHub shall be tested. Therefore, we have devised the following project:  
We simulate a road network where - surprise surprise - cars are driving. Upon completion of the project, the cars should autonomously find their way to a new destination and then seek a new one. It is particularly important that they consider other drivers to avoid accidents.
## How is the project structured?
### The project consists of 7 source code files:
#### 🚗 main.py
>This file brings together the others and contains the main loop of our project.
#### 🚗 event-handler.py
>This file manages keyboard and mouse inputs and checks if the program has been terminated.
#### 🚗 map-handler.py
>This file handles everything related to the map, from reading and analyzing to displaying on the corresponding surfaces.
#### 🚗 surface-handler.py
>This file contains the different surfaces and the functions related to them.
#### 🚗 tiles.py
>This file handles the different pixels (road and buildings) and their correct representation.
#### 🚗 vehicles.py
>This file contains the car class, which in turn contains all the functions for movement and display.
#### 🚗 pathfinder.py
>This file contains the pathfinding algorithm that the cars use to get from point A to point B.

### Furthermore, there are 3 directories:
#### 🚕 car_sprites
> This contains the images of the cars, named c_ plus a number. The came will randomly choose between all images in this directory when a car is generated.
#### 🚕 maps
> This contains the maps, made of a black pixel for street and a green one for buildings. The bigger the map, the longer the loading process will take. A map bigger than 200x200 px may be too big to calculate.
#### 🚕 tiles
> This contains the sprites for the streets an buildings. The buildings are seperated in sub-directories for different building sizes.
