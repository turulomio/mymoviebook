What is mymoviebook
===================
It's a script to generate your personal movie collection book. 

This book is interactive and lets you find your movies quickly in a book with your prefered movie images.

It uses postgres as your movie database

Usage
=====

MyMovieBook uses PostgreSQL database as its backend, so we must create a new database. To do it we just have to input the next command:

`mymoviebook --createdb`

By default it uses mymoviebook database, but we can change database connection parameters with:
*  --user USER         Postgresql user
*  --port PORT         Postgresql server port
*  --server SERVER     Postgresql server address
*  --db DB             Postgresql database

MyMovieBook it's prepared to create big books with thousands of films. So, in order to do this managemente easy, It's very important that movies are placed in numbered directories with 6 movies and its 6 covers.




Once installed, you can see man documentation with

`man mymoviebook`

License
=======
GPL-3

Links
=====

Source code & Development:
    https://github.com/Turulomio/mymoviebook

Doxygen documentation:
    http://turulomio.users.sourceforge.net/doxygen/mymoviebook/

Main developer web page:
    http://turulomio.users.sourceforge.net/en/proyectos.html
    
Pypi web page:
    https://pypi.org/project/mymoviebook/

Gentoo ebuild
    You can find a Gentoo ebuild in https://sourceforge.net/p/xulpymoney/code/HEAD/tree/myportage/media-video/mymoviebook/


Dependencies
============
* https://www.python.org/, as the main programming language.
* https://pypi.org/project/colorama/, to give console colors.
* Latex

Changelog
=========
1.3.0
-----
- Added the number of films in report for each year. Fixes #12.
- Now fimaffinity url is correctly encoded from name. Fixes #14.
- Printing film title shows the year too
- Added --createdb parameter to create a new database and load schema. Fixes #8.

1.2.1
-----
- Added png to MANIFEST

1.2.0
-----
- Spanish translation finished
- Removed table of contents from book
- Added filmaffinity querys clicking in covers

1.1.0
-----
- Add cover to the generated book
- Removing large objects from database. Covers are now in a bytes field.
- Added database update system
- Changed project icons
- Improved gettext translations
- Basic ODT format support

1.0.0
-----
- Created a python package from my pdffilms.py script


0.10.0
------
- Added the number of films in the list.

0.9.0
-----
- Fixed alphabetical sorting
- Added refs to DVD from individual films
