What is mymoviebook
===================
It's a script to generate your personal movie collection book. 

This book is interactive and lets you find your movies quickly in a book with your prefered movie images.

This is a page of automatically generated movie collection:

[![Demo](https://raw.githubusercontent.com/Turulomio/mymoviebook/master/doc/demo.jpg)](https://raw.githubusercontent.com/Turulomio/mymoviebook/master/doc/demo.pdf)

Linux installation
==================

If you use Gentoo, you can find the ebuild in https://github.com/turulomio/myportage/tree/master/media-video/mymoviebook

Or you can install with pypi, writing:

`pip install mymoviebook`

Or you can install from sources:

`poetry install`

You also need to install Latex in your distribution to be able to use `pdflatex` command


Usage
=====

MyMovieBook has Django as its backend, and uses a sqlite database by default. You can change it to use any django supported database. To prepare just run:

`mymoviebook --updatedb`

You can change your database settings using dj-database-url project https://github.com/jazzband/dj-database-url#url-schema

MyMovieBook it's prepared to create big books with thousands of films. So, in order to do this managemente easy, It's very important that movies are placed in numbered directories with 6 movies and its 6 covers. Although it's optional, I recommend to apped the year of the film to the end of the title.

For example, this is the content of a directory named /Films/7/

    -rw-r--r-- 1 user user 3096243290 ene  2 18:37 'Descalzos por el parque. 1967.avi' 
    -rw-r--r-- 1 user user      98977 ene  2 09:08 'Descalzos por el parque. 1967.jpg'
    -rw-r--r-- 1 user user     101423 ene  2 09:07 'El diablo dijo no. 1943.jpg'
    -rw-r--r-- 1 user user 2066396474 ene  2 19:28 'El diablo dijo no. 1943.mkv'
    -rw-r--r-- 1 user user     136564 ene  2 10:43 'El disputado voto del señor Cayo. 1985.jpg'
    -rw-r--r-- 1 user user 1777303444 ene  2 19:32 'El disputado voto del señor Cayo. 1985.mkv'
    -rw-r--r-- 1 user user 1856114688 ene  2 20:00 'El estado de la unión. 1948.avi'
    -rw-r--r-- 1 user user      80461 ene  2 09:39 'El estado de la unión. 1948.jpg'
    -rw-r--r-- 1 user user      68861 ene  2 08:54 'El manantial. 1949.jpg'
    -rw-r--r-- 1 user user 2460711108 ene  2 18:29 'El manantial. 1949.mkv'
    -rw-r--r-- 1 user user 2026502144 ene  2 19:35 'En un lugar solitario. 1950.avi'
    -rw-r--r-- 1 user user      97493 ene  2 09:26 'En un lugar solitario. 1950.jpg'

We enter in the directory with

`cd /Films/7`

We add the directory movie information to the database automatically, with the following command

`mymoviebook --insert`

If we need other parameters to connect to our database we can use them too.

We can add as many directories as we want.

Generating book movie
---------------------

Once all our movies are quickly added to database and if our latex is working (pdflatex command is needed), after executing

`mymoviebook --report /home/user/mymoviebook.pdf`

we get our movie collection book. This is the ![demo movie book](https://raw.githubusercontent.com/Turulomio/mymoviebook/master/doc/demo.pdf).


Links
=====

Doxygen documentation:
    https://coolnewton.mooo.com/doxygen/mymoviebook/

Pypi web page:
    https://pypi.org/project/mymoviebook/

Changelog
=========
1.10.0 (2023-04-22)
-------------------
- Code is now based in a standalone django process

1.9.0 (2022-11-13)
------------------
-  --insert parameter now checks there aren't more than 6 films per directory

1.8.0
-----
- Replaced officegenerator by unogenerator

1.7.0
-----
- Fixed error parsing names
- Improved objects encapsulation

1.6.0
-----
- Replaced --output and --generate parameter by --report
- Improved code structure

1.5.1
-----
- Removed demo files from distribution package.

1.5.0
-----
- Films without year are showed in PDF report.
- Duplicated films are showed in PDF report.

1.4.0
-----
- Captured error pressing CTRL+C
- Improved documentation and spanish translation

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
