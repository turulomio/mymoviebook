from gettext import translation
from importlib.resources import files
from mymoviebook import __version__
from mymoviebook.reusing.github import download_from_github
from os import system, environ
from sys import argv

try:
    t=translation('mymoviebook', files("mymoviebook") / "locale")
    _=t.gettext
except:
    _=str
def reusing():
    """
        Actualiza directorio reusing
        poe reusing
        poe reusing --local
    """
    local=False
    if len(argv)==2 and argv[1]=="--local":
        local=True
        print("Update code in local without downloading was selected with --local")
    if local==False:
        download_from_github("turulomio", "reusingcode", "python/casts.py", "mymoviebook/reusing")
        download_from_github("turulomio", "reusingcode", "python/github.py", "mymoviebook/reusing")
        download_from_github("turulomio", "reusingcode", "python/text_inputs.py", "mymoviebook/reusing")

def django_manage():
    """
        Allos to use django manage.py
    """
    environ.setdefault("DJANGO_SETTINGS_MODULE", "mymoviebook.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(argv)


def release():
        print(_("New Release:"))
        print(_("  * Change version and date in __init__.py"))
        print(_("  * Change version and date in pyproject.toml"))
        print(_("  * Edit Changelog in README"))
        print("  * poe translate")
        print("  * mcedit mymoviebook/locale/es.po")
        print("  * poe translate")
        print("  * poetry install")
#        print("  * python setup.py doxygen")
        print("  * git commit -a -m 'mymoviebook-{}'".format(__version__))
        print("  * git push")
        print(_("  * Make a new tag in github"))
        print("  * poetry build")
        print("  * poetry publish --username turulomio --password")
        print(_("  * Create a new gentoo ebuild with the new version"))
        print(_("  * Upload to portage repository")) 

def translate():
        #es
        system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o mymoviebook/locale/mymoviebook.pot mymoviebook/*.py")
        system("msgmerge -N --no-wrap -U mymoviebook/locale/es.po mymoviebook/locale/mymoviebook.pot")
        system("msgfmt -cv -o mymoviebook/locale/es/LC_MESSAGES/mymoviebook.mo mymoviebook/locale/es.po")
        system("msgfmt -cv -o mymoviebook/locale/fr/LC_MESSAGES/mymoviebook.mo mymoviebook/locale/fr.po")

#
### Class to define doxygen command
#class Doxygen(Command):
#    description = "Create/update doxygen documentation in doc/html"
#
#    user_options = [
#      # The format is (long option, short option, description).
#      ( 'user=', None, 'Remote ssh user'),
#      ( 'directory=', None, 'Remote ssh path'),
#      ( 'port=', None, 'Remote ssh port'),
#      ( 'server=', None, 'Remote ssh server'),
#  ]
#
#    def initialize_options(self):
#        self.user="root"
#        self.directory="/var/www/html/doxygen/mymoviebook/"
#        self.port=22
#        self.server="127.0.0.1"
#
#    def finalize_options(self):
#        pass
#
#    def run(self):
#        print("Creating Doxygen Documentation")
#        os.system("""sed -i -e "41d" doc/Doxyfile""")#Delete line 41
#        os.system("""sed -i -e "41iPROJECT_NUMBER         = {}" doc/Doxyfile""".format(__version__))#Insert line 41
#        os.system("rm -Rf build")
#        os.chdir("doc")
#        os.system("doxygen Doxyfile")      
#        command=f"""rsync -avzP -e 'ssh -l {self.user} -p {self.port} ' html/ {self.server}:{self.directory} --delete-after"""
#        print(command)
#        os.system(command)
#        os.chdir("..")
#
#
#class Doc(Command):
#    description = "Update man pages and translations"
#    user_options = [
#      # The format is (long option, short option, description).
#      ( 'user=', None, 'Database user'),
#      ( 'db=', None, 'Database name'),
#      ( 'port=', None, 'Database port'),
#      ( 'server=', None, 'Database server'),
#  ]
#    def initialize_options(self):
#        self.user="postgres"
#        self.db="mymoviebook"
#        self.port="5432"
#        self.server="127.0.0.1"
#
#    def finalize_options(self):
#        pass
#
#    def run(self):
#        from mymoviebook.reusing.connection_pg import Connection
#        con=Connection()
#        con.user=self.user
#        con.server=self.server
#        con.port=self.port
#        con.db=self.db
#        con.get_password("", "")
#        con.connect()
#        print("Is connection active?",  con.is_active())
#        #es
#        os.system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o locale/mymoviebook.pot *.py mymoviebook/*.py mymoviebook/objects/*.py")
#        os.system("msgmerge -N --no-wrap -U locale/es.po locale/mymoviebook.pot")
#        os.system("msgmerge -N --no-wrap -U locale/fr.po locale/mymoviebook.pot")
#        os.system("msgfmt -cv -o mymoviebook/locale/es/LC_MESSAGES/mymoviebook.mo locale/es.po")
#        os.system("msgfmt -cv -o mymoviebook/locale/fr/LC_MESSAGES/mymoviebook.mo locale/fr.po")
#
#        for language in ["en", "es", "fr"]:
#            self.mangenerator(language)
#
#        print("Updating Entity Relationship Schema")
#        os.chdir("doc/html")
#        os.system("/usr/bin/postgresql_autodoc -d {} -h {} -u {} -p {} --password={} -t html".format(self.db,self.server,self.user, self.port,con.password))
#        os.system("/usr/bin/postgresql_autodoc -d {} -h {} -u {} -p {} --password={} -t dot_shortfk".format(self.db,self.server,self.user, self.port,con.password))
#        os.system("dot -Tpng {0}.dot_shortfk -o {0}_er.png".format(self.db))
#
#
#    def mangenerator(self, language):
#        """
#            Create man pages for parameter language
#        """
#        from mangenerator import Man
#        if language=="en":
#            lang1=gettext.install('mymoviebook', 'badlocale')
#            man=Man("man/man1/mymoviebook")
#        else:
#            lang1=gettext.translation('mymoviebook', 'mymoviebook/locale', languages=[language])
#            lang1.install()
#            man=Man("man/{}/man1/mymoviebook".format(language))
#        print("  - DESCRIPTION in {} is {}".format(language, _("DESCRIPTION")))
#
#        man.setMetadata("mymoviebook",  1,   datetime.date.today(), "Mariano Muñoz", _("Change files and directories owner and permissions recursively."))
#        man.setSynopsis("""usage: mymoviebook [-h] [--version] [--insert | --generate] [--user USER]
#                   [--port PORT] [--host HOST] [--db DB] [--output OUTPUT]
#                   [--format {PDF}]""")
#        man.header(_("DESCRIPTION"), 1)
#        man.paragraph(_("This app has the following mandatory parameters:"), 1)
#        man.paragraph("--insert", 2, True)
#        man.paragraph(_("Inserts a directory with movies with the index of the last directory numeric name."), 3)
#        man.paragraph("--report", 2, True)
#        man.paragraph(_("Generates the movie collection document"), 3)
#        man.paragraph(_("Path where the movie book it's going to be generated. You can use this parameter as many times as you want."), 3)
#
#        man.paragraph(_("Postgresql database connection parameters:"), 1)
#        man.paragraph("--user", 2, True)
#        man.paragraph(_("User of the database. By default 'postgres'." ), 3)
#        man.paragraph("--port", 2, True)
#        man.paragraph(_("Database port. By default '5432'"), 3)
#        man.paragraph("--host", 2, True)
#        man.paragraph(_("Database server. By default '127.0.0.1'."), 3)
#        man.paragraph("--db", 2, True)
#        man.paragraph(_("Database name. By default 'mymoviebook'."), 3)
#        man.paragraph("--format", 2, True)
#        man.paragraph(_("You can choose PDF or ODT arguments. PDF is used by default."), 3)
#
#        man.header(_("EXAMPLES"), 1)
#        man.paragraph(_("Insert movies with index 23"), 2, True)
#        man.paragraph("mymoviebook --insert /path/to/my/movies/23", 3)
#        man.paragraph(_("This command insert in database all movies (up to 6) in 23 directory. Each film must have it's cover with the same filename."), 3)
#        man.paragraph(_("Generate a book with all movies in the database in two different directories"), 2, True)
#        man.paragraph("mymoviebook --report /home/user/mymoviecollection.pdf  --report /home/user2/mymoviecollection.pdf", 3)
#        man.paragraph(_("This command generates your movie book in the report path."), 3)
#        man.save()
#
#
#
#class Reusing(Command):
#    description = "Fetch remote modules"
#    user_options = [
#      # The format is (long option, short option, description).
#      ( 'local', None, 'Update files without internet'),
#  ]
#
#    def initialize_options(self):
#        self.local=False
#
#    def finalize_options(self):
#        pass
#
#    def run(self):
#        from sys import path
#        path.append("mymoviebook/reusing")
#        print(self.local)
#        if self.local is False:
#            from github import download_from_github
#            download_from_github('turulomio','reusingcode','python/admin_pg.py', 'mymoviebook/reusing')
#            download_from_github('turulomio','reusingcode','python/file_functions.py', 'mymoviebook/reusing')
#            download_from_github('turulomio','reusingcode','python/call_by_name.py', 'mymoviebook/reusing') 
#            download_from_github('turulomio','reusingcode','python/casts.py', 'mymoviebook/reusing')
#            download_from_github('turulomio','reusingcode','python/datetime_functions.py', 'mymoviebook/reusing')
#            download_from_github('turulomio','reusingcode','python/decorators.py', 'mymoviebook/reusing')
#            download_from_github('turulomio','reusingcode','python/github.py', 'mymoviebook/reusing')
#            download_from_github('turulomio','reusingcode','python/libmanagers.py', 'mymoviebook/reusing')
#            download_from_github('turulomio','reusingcode','python/connection_pg.py', 'mymoviebook/reusing')
#            download_from_github('turulomio','reusingcode','python/text_inputs.py', 'mymoviebook/reusing')
#        
#        from file_functions import replace_in_file
#        replace_in_file("mymoviebook/reusing/libmanagers.py","from datetime_functions","from .datetime_functions")
#        replace_in_file("mymoviebook/reusing/libmanagers.py","from call_by_name","from .call_by_name")
#




#class Video(Command):
#    description = "Create video/GIF from console ouput"
#    user_options = ['--compile']
#
#    def initialize_options(self):
#        pass
#
#    def finalize_options(self):
#        pass
#
#    def run(self):
#        print(_("You need ttyrecgenerator installed to generate videos"))
#        os.chdir("doc/ttyrec")
#        os.system("ttyrecgenerator --output mymoviebook_howto_es 'python3 howto.py' --lc_all es_ES.UTF-8")
#        os.system("ttyrecgenerator --output mymoviebook_howto_en 'python3 howto.py' --lc_all C")
#        os.chdir("../..")
#
#    ########################################################################
#
#
