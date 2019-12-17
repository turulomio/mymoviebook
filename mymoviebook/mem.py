from mymoviebook.connection_pg import Connection, argparse_connection_arguments_group
from pkg_resources import resource_filename
from argparse import ArgumentParser, RawTextHelpFormatter
from gettext import translation
from shutil import rmtree
from os import system, mkdir, path
from signal import signal, SIGINT
from sys import exit
from mymoviebook.version import __version__, __versiondate__


class Mem:
    def __init__(self):
        signal(SIGINT, self.signal_handler)
        self.con=Connection()
        self.create_parser()
        self.create_args_from_parser()
        
    def _(self, s ):
        t=translation('mymoviebook', resource_filename("mymoviebook","locale"))
        return t.gettext(s)
                
    def signal_handler(self, signal, frame):
            print(self._("You pressed 'Ctrl+C', exiting..."))
            exit(1)
            
    def create_parser(self):
        self.parser=ArgumentParser(prog='mymoviebook', description=self._('Generate your personal movie collection book'), epilog=self._("Developed by Mariano Muñoz 2012-{}".format(__versiondate__.year) + " \xa9"), formatter_class=RawTextHelpFormatter)
        self.parser.add_argument('--version', action='version', version=__version__)

        group = self.parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--insert', help=self._('Insert films from current numbered directory'), action="store_true", default=False)
        group.add_argument('--report', help=self._('Films report is generated in this path. Can be called several times'), action="append", default=[])
        group.add_argument('--createdb', help=self._("Creates a new postgresql database, checking if already exists. Copy MyMovieBook schema on it"), action="store_true", default=False)

        argparse_connection_arguments_group(self.parser, gettext_module="mymoviebook",  gettex_locale=resource_filename("mymoviebook","locale"), default_db="mymoviebook") 

        group_generate=self.parser.add_argument_group(self._("Other parameters"))
        group_generate.add_argument('--format', help=self._("select output format. Default is PDF"), action="store", choices=['PDF', 'ODT'],  default='PDF')
        
    def create_args_from_parser(self, parameters=None):
        #Validations
        self.args=self.parser.parse_args(parameters)
        for file in self.args.report:
            if path.isdir(file)==True:
                print("--report parameter can't be a directory ({})".format(file))
                exit(1)

    ##Must be called after parser
    def create_connection(self):
        self.con.user=self.args.user
        self.con.server=self.args.server
        self.con.port=self.args.port
        self.con.db=self.args.db
        self.con.get_password(gettext_module="mymoviebook",  gettex_locale=resource_filename("mymoviebook","locale")) 
        self.con.connect()
        if self.con.is_active()==False:
            exit(1)

    ##Without dateabase
    ##Must be called after parser
    def create_admin_pg(self):
        from mymoviebook.admin_pg import AdminPG
        self.con.user=self.args.user
        self.con.server=self.args.server
        self.con.port=self.args.port
        self.con.db=self.args.db
        password=self.con.get_password(gettext_module="mymoviebook",  gettex_locale=resource_filename("mymoviebook","locale")) 
        self.admin=AdminPG(self.args.user, password, self.args.server, self.args.port)

    def create_temporal_directory(self):
        try:
            rmtree("/tmp/mymoviebook")
        except:
            pass
        mkdir("/tmp/mymoviebook")
        system("chmod 777 /tmp/mymoviebook")
        
        
    
    def remove_temporal_directory(self):
        rmtree("/tmp/mymoviebook")
