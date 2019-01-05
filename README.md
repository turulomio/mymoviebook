What is mymoviebook
===================
It's a script to generate your personal movie collection book. 

This book is interactive and lets you find your movies quickly in a book with your prefered movie images.

It uses postgres as your movie database

Usage
=====

Here you have a console video example:

![English howto](https://raw.githubusercontent.com/Turulomio/mymoviebook/master/doc/ttyrec/mymoviebook_howto_en.gif)

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
