from setuptools import setup, Command
import datetime
import gettext
import os
import platform
import site

gettext.install('recpermissions', 'recpermissions/locale')

class Doxygen(Command):
    description = "Create/update doxygen documentation in doc/html"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print("Creating Doxygen Documentation")
        os.system("""sed -i -e "41d" doc/Doxyfile""")#Delete line 41
        os.system("""sed -i -e "41iPROJECT_NUMBER         = {}" doc/Doxyfile""".format(__version__))#Insert line 41
        os.system("rm -Rf build")
        os.chdir("doc")
        os.system("doxygen Doxyfile")
        os.system("rsync -avzP -e 'ssh -l turulomio' html/ frs.sourceforge.net:/home/users/t/tu/turulomio/userweb/htdocs/doxygen/recpermissions/ --delete-after")
        os.chdir("..")

class Procedure(Command):
    description = "Create/update doxygen documentation in doc/html"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(_("New Release:"))
        print(_("  * Change version and date in version.py"))
        print(_("  * Edit Changelog in README"))
        print("  * python setup.py doc")
        print("  * mcedit locale/es.po")
        print("  * python setup.py doc")
        print("  * python setup.py install")
        print("  * python setup.py doxygen")
        print("  * mcedit doc/ttyrec/howto.py")
        print("  * python setup.py video" + ". " + _("If changed restart from first python setup.py doc"))
        print("  * git commit -a -m 'recpermissions-X.X.X'")
        print("  * git push")
        print(_("  * Make a new tag in github"))
        print("  * python setup.py sdist upload -r pypi")
        print(_("  * Create a new gentoo ebuild with the new version"))
        print(_("  * Upload to portage repository")) 

class Uninstall(Command):
    description = "Uninstall installed files with install"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if platform.system()=="Linux":
            os.system("rm -Rf {}/recpermissions*".format(site.getsitepackages()[0]))
            os.system("rm /usr/bin/recpermissions")
            os.system("rm /usr/share/man/man1/recpermissions.1")
            os.system("rm /usr/share/man/es/man1/recpermissions.1")
        else:
            print(_("Uninstall command only works in Linux"))

class Doc(Command):
    description = "Update man pages and translations"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        #es
        os.system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o locale/recpermissions.pot *.py recpermissions/*.py doc/ttyrec/*.py")
        os.system("msgmerge -N --no-wrap -U locale/es.po locale/recpermissions.pot")
        os.system("msgmerge -N --no-wrap -U locale/fr.po locale/recpermissions.pot")
        os.system("msgfmt -cv -o recpermissions/locale/es/LC_MESSAGES/recpermissions.mo locale/es.po")
        os.system("msgfmt -cv -o recpermissions/locale/fr/LC_MESSAGES/recpermissions.mo locale/fr.po")

        for language in ["en", "es", "fr"]:
            self.mangenerator(language)

    def mangenerator(self, language):
        """
            Create man pages for parameter language
        """
        from mangenerator import Man
        if language=="en":
            lang1=gettext.install('recpermissions', 'badlocale')
            man=Man("man/man1/recpermissions")
        else:
            lang1=gettext.translation('recpermissions', 'recpermissions/locale', languages=[language])
            lang1.install()
            man=Man("man/{}/man1/recpermissions".format(language))
        print("  - DESCRIPTION in {} is {}".format(language, _("DESCRIPTION")))

        man.setMetadata("RecPermissions",  1,   datetime.date.today(), "Mariano Muñoz", _("Change files and directories owner and permissions recursively."))
        man.setSynopsis("""usage: recpermissions [-h] [--version] [--user USER] [--group GROUP]
                      [--files PERM] [--directories PERM] [--remove_emptydirs]
                      [--only]
                      absolute_path""")
        man.header(_("DESCRIPTION"), 1)
        man.paragraph(_("This app has the following mandatory parameters:"), 1)
        man.paragraph("--user", 2, True)
        man.paragraph(_("User used to change files owner.") + " " + _("It does nothing if it's not set"), 3)
        man.paragraph("--group", 2, True)
        man.paragraph(_("Group used to change files owner group.") + " " + _("It does nothing if it's not set"), 3)
        man.paragraph("--files", 2, True)
        man.paragraph(_("File permissions in octal to be used.") + " " + _("It does nothing if it's not set"), 3)
        man.paragraph("--directories", 2, True)
        man.paragraph(_("Directory permissions in octal to be used.") + " " + _("It does nothing if it's not set"), 3)
        man.paragraph("--remove_emptydirs", 2, True)
        man.paragraph(_("When used in script, removes all empty dirs recursively from path."), 3)
        man.paragraph("--only", 2, True)
        man.paragraph(_("Only changes permissions to the file or directory passed in absolute_path parameter."), 3)
        man.paragraph("absolute_path", 2, True)
        man.paragraph(_("To avoid errors and wrong changes, path must be an absolute one."), 3)  
        man.header(_("EXAMPLES"), 1)
        man.paragraph(_("Null Example"), 2, True)
        man.paragraph(_("recpermissions /home/user/"), 3)
        man.paragraph(_("This comand does nothing"), 3)
        man.paragraph(_("Partial Example"), 2, True)
        man.paragraph(_("recpermissions --user user --files 644 /home/user/"), 3)
        man.paragraph(_("This command only changes user permissions and files permissions to 644. Group and directory permissions are not changed:"), 3)
        man.paragraph(_("Full Example"), 2, True)
        man.paragraph(_("recpermissions --user root --group root --files 640 --directories 750 --remove_emptydirs /home/user/"), 3)
        man.paragraph(_("This command will change user and group to root user and group. Files will have rw-r----- permisions and directories rwxr-x--- permisions. If the script finds empty dirs it will remove them:"), 3)
        man.paragraph(_("Only Example"), 2, True)
        man.paragraph(_("recpermissions --user user /home/user/README.txt --only"), 3)
        man.paragraph(_("This command will change user ownership to the file /home/usr/README.txt only"),  3)
        man.save()

class Video(Command):
    description = "Create video/GIF from console ouput"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(_("You need ttyrecgenerator installed to generate videos"))
        os.chdir("doc/ttyrec")
        os.system("ttyrecgenerator --output recpermissions_howto_es 'python3 howto.py' --lc_all es_ES.UTF-8")
        os.system("ttyrecgenerator --output recpermissions_howto_en 'python3 howto.py' --lc_all C")
        os.chdir("../..")

    ########################################################################


## Version of modele captured from version to avoid problems with package dependencies
__version__= None
with open('recpermissions/version.py', encoding='utf-8') as f:
    for line in f.readlines():
        if line.find("__version__ =")!=-1:
            __version__=line.split("'")[1]


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

if platform.system()=="Linux":
    data_files=[('/usr/share/man/man1/', ['man/man1/recpermissions.1']), 
                ('/usr/share/man/es/man1/', ['man/es/man1/recpermissions.1'])
               ]
else:
    data_files=[]

setup(name='recpermissions',
    version=__version__,
    description='Change files and directories permisions and owner recursivily from current directory',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: System Administrators',
                 'Topic :: System :: Systems Administration',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Programming Language :: Python :: 3',
                ],
    keywords='change permissions ownner files directories',
    url='https://github.com/Turulomio/recpermissions',
    author='Turulomio',
    author_email='turulomio@yahoo.es',
    license='GPL-3',
    packages=['recpermissions'],
    entry_points = {'console_scripts': ['recpermissions=recpermissions.core:main',
                                       ],
                   },
    install_requires=['colorama','setuptools'],
    data_files=data_files,
    cmdclass={ 'doxygen': Doxygen,
               'doc': Doc,
               'uninstall': Uninstall,
               'video': Video,
               'procedure': Procedure,
             },
    zip_safe=False,
    include_package_data=True
    )

_=gettext.gettext#To avoid warnings
