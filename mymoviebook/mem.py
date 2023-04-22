from argparse import ArgumentParser, RawTextHelpFormatter
from django.conf import settings
from gettext import translation
from os import path
from signal import signal, SIGINT
from sys import exit
from mymoviebook import __version__, __versiondate__
from importlib.resources import files

try:
    t=translation('mymoviebook', files("mymoviebook") / "locale")
    _=t.gettext
except:
    _=str

class Mem:
    def __init__(self):
        signal(SIGINT, self.signal_handler)
        self.create_parser()
        self.create_args_from_parser()

                
    def signal_handler(self, signal, frame):
            print(_("You pressed 'Ctrl+C', exiting..."))
            exit(1)
            
    def create_parser(self):
        self.parser=ArgumentParser(prog='mymoviebook', description=_('Generate your personal movie collection book'), epilog=_("Developed by Mariano Muñoz 2012-{}".format(__versiondate__.year) + " \xa9"), formatter_class=RawTextHelpFormatter)
        self.parser.add_argument('--version', action='version', version=__version__)
        self.parser.add_argument('--debug', help=_('Debug mode'), action="store_true", default=False)

        group = self.parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--insert', help=_('Insert films from current numbered directory'), action="store_true", default=False)
        group.add_argument('--report', help=_('Films report is generated in this path. Can be called several times'), action="append", default=[])
        group.add_argument('--createdb', help=_("Creates a new postgresql database, checking if already exists. Copy MyMovieBook schema on it"), action="store_true", default=False)
        group_generate=self.parser.add_argument_group(_("Other parameters"))
        group_generate.add_argument('--format', help=_("select output format. Default is PDF"), action="store", choices=['PDF'],  default='PDF')

        group_db=self.parser.add_argument_group(_("Postgres database connection parameters"))
        group_db.add_argument('--user', help=_('Postgresql user'), default="postgres")
        group_db.add_argument('--port', help=_('Postgresql server port'), default="5432")
        group_db.add_argument('--server', help=_('Postgresql server address'), default="127.0.0.1")
        group_db.add_argument('--db', help=_('Postgresql database'), default="mymoviebook")

    def create_args_from_parser(self, parameters=None):
        #Validations
        self.args=self.parser.parse_args(parameters)
        for file in self.args.report:
            if path.isdir(file)==True:
                print("--report parameter can't be a directory ({})".format(file))
                exit(1)

        settings.DATABASES["default"]["NAME"]=self.args.db
        settings.DATABASES["default"]["USER"]=self.args.user
        settings.DATABASES["default"]["PORT"]=self.args.port
        settings.DATABASES["default"]["SERVER"]=self.args.server
        settings.DEBUG=self.args.debug
