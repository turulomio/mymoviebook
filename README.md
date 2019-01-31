What is mymoviebook
===================
It's a script to generate your personal movie collection book. 

This book is interactive and lets you find your movies quickly in a book with your prefered movie images.

It uses postgres as your movie database

Usage
=====

MyMovieBook uses PostgreSQL database as its backend, so we must create a new database and load the schema needed. To do it we just have to input the next command:

`mymoviebook --createdb`

By default it uses mymoviebook database, but we can change database connection parameters with:
*  --user USER         Postgresql user
*  --port PORT         Postgresql server port
*  --server SERVER     Postgresql server address
*  --db DB             Postgresql database

MyMovieBook it's prepared to create big books with thousands of films. So, in order to do this managemente easy, It's very important that movies are placed in numbered directories with 6 movies and its 6 covers. Although it's optional, I recommend to apped the year of the film to the end of the title.

For example, this is the content of a directory named /Films/7/

    -rw-r--r-- 1 keko keko 3096243290 ene  2 18:37 'Descalzos por el parque. 1967.avi' 
    -rw-r--r-- 1 keko keko      98977 ene  2 09:08 'Descalzos por el parque. 1967.jpg'
    -rw-r--r-- 1 keko keko     101423 ene  2 09:07 'El diablo dijo no. 1943.jpg'
    -rw-r--r-- 1 keko keko 2066396474 ene  2 19:28 'El diablo dijo no. 1943.mkv'
    -rw-r--r-- 1 keko keko     136564 ene  2 10:43 'El disputado voto del señor Cayo. 1985.jpg'
    -rw-r--r-- 1 keko keko 1777303444 ene  2 19:32 'El disputado voto del señor Cayo. 1985.mkv'
    -rw-r--r-- 1 keko keko 1856114688 ene  2 20:00 'El estado de la unión. 1948.avi'
    -rw-r--r-- 1 keko keko      80461 ene  2 09:39 'El estado de la unión. 1948.jpg'
    -rw-r--r-- 1 keko keko      68861 ene  2 08:54 'El manantial. 1949.jpg'
    -rw-r--r-- 1 keko keko 2460711108 ene  2 18:29 'El manantial. 1949.mkv'
    -rw-r--r-- 1 keko keko 2026502144 ene  2 19:35 'En un lugar solitario. 1950.avi'
    -rw-r--r-- 1 keko keko      97493 ene  2 09:26 'En un lugar solitario. 1950.jpg'

We enter in the directory with

`cd /Films/7`

we add the directory to the database with. If we need other parameters to connect to our database we can use them too.

`mymoviebook --insert`

We can add as many directories as we want.

If our latex is working, after executing

`mymoviebook --generate --output /home/user/mymoviebook.pdf`

we get our movie collection book. This is a ![demo](https://raw.githubusercontent.com/Turulomio/mymoviebook/master/doc/demo.pdf).


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
