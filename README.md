# nba-biplayer-statistics

nba-biplayer-statistics is a project made to analyze and visualize results of pairs of NBA players.

## overview

The project consists of five core .py files: docs, utils, parsing, visualizing and main. Docs is a completely technical module, used to type-check arguments of
functions in the rest of the modules. Utils provides various utility functions, largely serving to make other modules – which obviously use the functions 
defined in utils – more concise. Parsing is the backbone of the project, responsible for accessing, cleaning and analyzing data stored on espn.com. Visualizing
is what turns massive DataFrames into aesthetically-pleasing charts, storing every function in charge of drawing the result. Finally, main is the driver module 
linking it all together: the smallest one of the five, it parses and visualizes data relying on four other modules.

## requirements

In addition to everything Python provides out of the box, the following modules and libraries are required for this project to work:
* imageio – used to create the final gif.
* matplotlib – self-explanatory.
* numpy – self-explanatory.
* pandas – self-explanatory.
* pydoc – used to type-check arguments.

Also, Python 3.6 at least is required to make f-strings works.

## installation

As of right now, this project is sadly not available on pip. To use it, you should download the files and run it on your system.

## license

[MIT](https://choosealicense.com/licenses/mit/)
