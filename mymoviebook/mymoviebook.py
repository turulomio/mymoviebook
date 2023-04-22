from sys import exit
from pkg_resources import resource_filename
from mymoviebook.reusing.dbupdates import UpdateDB
from mymoviebook.mem import Mem
from mymoviebook.objects.films import FilmManager_from_db_query, add_movies_to_database
from os import environ

### MAIN SCRIPT ###
def main(parameters=None):
    environ.setdefault("DJANGO_SETTINGS_MODULE", "mymoviebook.settings")

    #instantiate a web sv for django which is a wsgi
    from django.core.wsgi import get_wsgi_application
    get_wsgi_application()

    from mymoviebook import models
    #import your models schema
    print(models.Films.objects.count())


    mem=Mem()

    if mem.args.createdb==True:
        mem.create_admin_pg()
        if mem.admin.db_exists(mem.args.db):
            print(mem._("I can't create '{}' database because it already exists.").format(mem.args.db))
        else:
            mem.admin.create_db(mem.args.db)
            con=mem.admin.connect_to_database(mem.args.db)
            con.load_script(resource_filename("mymoviebook","sql/mymoviebook.sql"))
            con.commit()
            print(mem._("MyMovieBook it's ready for use"))
        exit(0)

    mem.create_connection()
    UpdateDB(mem)
    
    mem.create_temporal_directory()

    if mem.args.insert==True:# insertar
        add_movies_to_database(mem)


    elif len(mem.args.report)>0:## Report arg
        # SACA LAS IMÁGENES DE LA BASE DE DATOS
        print ("  - "+ mem._("Getting images"))
        sf=FilmManager_from_db_query(mem, "SELECT * FROM films")
        sf.extract_photos()
        if mem.args.format=="PDF":
            sf.generate_pdf()
    else:
        mem.parser.print_help()

    mem.con.disconnect()

    mem.remove_temporal_directory()
