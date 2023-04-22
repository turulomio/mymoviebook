from mymoviebook.mem import Mem
from os import environ
from datetime import datetime, date
from gettext import translation
from glob import glob
from importlib.resources import files
from mymoviebook.reusing.casts import string2tex
from mymoviebook.reusing.text_inputs import input_YN
from mymoviebook import __version__
from os import system, getcwd, path
from pkg_resources import resource_filename
from tempfile import TemporaryDirectory
try:
    t=translation('mymoviebook', files("mymoviebook") / "locale")
    _=t.gettext
except:
    _=str

from django.db import connection
    
### MAIN SCRIPT ###
def main(parameters=None):
    #Before any django import
    environ.setdefault("DJANGO_SETTINGS_MODULE", "mymoviebook.settings")
    from django.core.wsgi import get_wsgi_application
    #instantiate a web sv for django which is a wsgi
    get_wsgi_application()    
    mem=Mem()
    
    if mem.args.insert==True:# insertar
        add_movies_to_database(mem)


    elif len(mem.args.report)>0:## Report arg
        if mem.args.format=="PDF":
            generate_pdf(mem)
    else:
        mem.parser.print_help()


## Returns a FilmManager with the films duplicated in the database
def films_duplicated(qs):
    result=[]
    qs=qs.order_by("name")
    last=None
    for f in qs:
        if last!=None and f.title()==last.title() and f.year()==last.year():
            result.append(f)
            result.append(last)
        last=f
    return result

##  This method can be used as a function when decorators are not allowed (DRF actions)
def show_queries_function():
    sum_=0
    for d in connection.queries:
        print (f"[{d['time']}] {d['sql']}")
        sum_=sum_+float(d['time'])
    print (f"{len(connection.queries)} db queries took {round(sum_*1000,2)} ms")
 
        
## Function to add movies to a database from console
def add_movies_to_database(mem):
    from mymoviebook import models
    try:
        cwd=getcwd().split("/")
        id=int(cwd[len(cwd)-1])
    except:
        print (mem._("Current directory is not numeric"))
        exit(100)

    if input_YN(mem._("The id of the directory to add is '{}'. Do you want to continue?").format(id))==False:
        exit(100)

    print ("+ " + mem._("Checking that the movies have the correct format..."))
    
    number_images=0
    for file in glob( getcwd()+ "/*.jpg" ):
        if path.exists(file[:-3]+"avi")==False and path.exists(file[:-3]+"mpg")==False and path.exists(file[:-3]+"mkv")==False:
            print (mem._("There isn't a movie with the same name '{}'").format(file[:-3]))
            exit(100)
        number_images=number_images+1
        
    #Check if there are more than 6 images
    print ("+ " + mem._("Checking the number of films in the directory..."))
    if number_images>6:
        print(mem._("There are more than 6 films in this directory. Please fix it."))
        exit(100)
        

    # "Chequeando si hay registros en la base de datos del dispositivo " + str(id)
    qs=models.Films.objects.filter(dvd=id)
    if qs.count()>0:
        if input_YN("+ " + mem._("Do you want to overwrite the information of directory '{}'?").format(id))==False:
            exit(100)
        else:
            print ("   - " + mem._("Deleting information..."))
            qs.delete()
            
    print ("+ "+ mem._("Adding movies to the database"))
    for file in glob( getcwd()+ "/*.jpg" ):
        film=models.Films()
        film.savedate=date.today()
        film.name=file[len(getcwd())+1:-4]
        film.dvd=id
        film.save()

        cover=models.Covers()
        cover.films=film
        cover.cover=open(file, "rb").read()
        cover.save()
        print ("    - {0}".format(file))



def generate_pdf(mem):
    
    from mymoviebook import models
    
    with TemporaryDirectory() as tmpdirname:
        print('created temporary directory', tmpdirname, )
        qs_films_all=models.Films.objects.all().select_related("covers").order_by("dvd")
        
        
        # SACA LAS IMÁGENES DE LA BASE DE DATOS
        print ("  - "+ _("Getting images"))    
        
        dict_dvds={}
        dict_years={}
        films_without_year=[]
        for film in qs_films_all:
            #Extract foto to tempdir
            film.covers.extract_to_path(tmpdirname)
            #Createds dvd dictionary
            if not film.dvd in dict_dvds:
                dict_dvds[film.dvd]=[]
            dict_dvds[film.dvd].append(film)
            #Creates year dictionary
            if film.year() is None:
                films_without_year.append(film)
                continue            
            if not film.year() in dict_years:
                dict_years[film.year()]=[]
            dict_years[film.year()].append(film)
        
        icon=resource_filename("mymoviebook","images/mymoviebook.png")


        header=""
        header = header + "\\documentclass[12pt,a4paper]{article}\n"
        header = header + "\\usepackage{pdflscape}\n"
        header = header + "\\usepackage[utf8]{inputenc}\n"
        header = header + "\\usepackage[spanish]{babel}\n"
        header = header + "\\usepackage[T1]{fontenc}\n"
        header = header + "\\usepackage{geometry}\n"
        header = header + "\\usepackage{setspace}\n"
        header = header + "\\usepackage{graphicx}\n"
        header = header + "\\usepackage{ae,aecompl}\n"
        header = header + "\\usepackage[bookmarksnumbered, colorlinks=true, urlcolor=blue, linkcolor=blue, pdftitle={"+ _("My movie book") +"}, pdfauthor={MyMovieBook-"+ __version__ +"}, pdfkeywords={movie book}]{hyperref}\n"
        header = header + "\\geometry{verbose,a4paper}\n"
        header = header + "\\usepackage{anysize}\n"
        header = header + "\\marginsize{1.5cm}{1.5cm}{0.5cm}{1cm} \n"
        header = header + "\\usepackage{array}\n"
        header = header + "\\begin{document}\n"
        header = header + "\\title{\\textbf{" + _("My movie book") + "}}\n"
        header = header + "\\author{MyMovieBook-"+ __version__ +"}\n"

        header = header + "\\setlength{\\parindent}{1cm}\n"
        header = header + "\\setlength{\\parskip}{0.2cm}\n"


        bd=""
        bd=bd + "\\maketitle\n"
        bd=bd + "\\addcontentsline{toc}{section}{"+ _("Title") +"}\n"

        bd=bd + "\\begin{center}\n"
        bd=bd + "\\includegraphics[width=3cm,height=3cm]{{{0}}}\n".format(icon)
        bd=bd + "\\end{center}\n"
        bd=bd + "\\par\n"
        bd=bd + "\\vspace{1cm}\n"

        bd=bd + _("This movie book has been generated using version {} of MyMovieBook.").format(__version__) +" " + _("It's an opensource application published under GPL-3 license.") + "\\par\n"
        bd=bd + _("The main page of the project is in \href{https://github.com/turulomio/mymoviebook}{GitHub}.")+ "\\par\n"
        bd=bd + _("This book has {} movies and it was generated at {}.").format(qs_films_all.count(), datetime.now().time()) +"\\par\n"
        bd=bd + _("If you make click over a film cover, you'll be redirected to FilmAffinity portal to try to get information of the movie.")
        bd=bd +"\\newpage\n"

        print ("  - " + _("List by index"))
        bd = bd + "\section{"+ _("Big covers") +"}\n"
        bd = bd + "\\setlength{\\parindent}{0cm}\n"
        list_dvds=list(dict_dvds.keys())
        list_dvds.sort()
        for dvd in reversed(list_dvds):
            bd=bd + "\\subsection*{"+ _("Index") + " " + str(dvd)+"}\n" 
            bd=bd + "\\label{{sec:{0}}}\n".format(dvd)
            bd=bd + "\\addcontentsline{toc}{subsection}{"+ _("Index") + " " + str(dvd)+"}\n" 
            
            bd=bd + "\\begin{center}\n"
            bd=bd + "\\begin{tabular}{c c}\n"
            for i, fi in enumerate(dict_dvds[dvd]):
                bd=bd+ "\\begin{tabular}{p{8cm}}\n" #Tabla foto name interior
                bd=bd+ fi.covers.tex(8,6.8) + "\\\\\n"
                bd=bd+ string2tex(fi) +"\\\\\n"
                bd=bd+ "\\end{tabular} &"
                if i % 2==1:
                    bd=bd[:-2]+"\\\\\n"
            bd = bd + "\\end{tabular}\n"
            bd=bd + "\\end{center}\n"
            bd=bd +"\n\\newpage\n\n"


        print (_("  - Films list with small covers"))
        bd = bd + "\\setlength{\\parindent}{0cm}\n"
        bd=bd + "\section{"+ _("Small covers") +"}\n"
        for dvd in reversed(list_dvds):
            bd=bd + "\\begin{tabular}{m{2cm} m{2cm} m{2cm} m{2cm} m{2cm} m{2cm} m{2cm}}\n"
            bd=bd + _("Index") + " " +str(dvd) + " & "
            for i, fi in enumerate(dict_dvds[dvd]):
                bd=bd + fi.covers.tex(2,2) + " &" 
            bd = bd[:-2]  + "\n"
            bd = bd + "\\end{tabular} \n\n"
        bd=bd +"\n\\newpage\n\n"

        print (_("  - Films list ordered by title"))
        bd=bd + "\section{"+_("Order by movie title") +"}\n"
        qs_films_all=qs_films_all.order_by("name")
        for f in qs_films_all:
            bd=bd + "\\subsection*{"+ string2tex(f) + "} \n"
            bd=bd + "\\addcontentsline{{toc}}{{subsection}}{{{0}}}\n".format(string2tex(f))
            bd=bd + f.covers.tex_tabular(show_name=False)
        bd=bd +"\\newpage\n\n"

        print ("  - Ordered by year films list")
        bd = bd + "\\setlength{\\parindent}{1cm}\n"
        bd=bd + "\section{"+ _("Order by movie year") + "}\n"
        
        list_years=list(dict_years.keys())
        print(list_years)
        list_years.sort()
        for year in list_years:
            if year!="None":
                bd=bd + "\\subsection*{"+ _("Year") +" " + str(year) +"}\n" 
                bd=bd + "\\addcontentsline{toc}{subsection}{" + _("Year") + " " + str(year) + "}\n" 
                
                if len(dict_years[year])==1:
                    bd = bd + _("There is only one collection film in this year:") + "\\par\n"
                elif len(dict_years[year])>1:
                    bd = bd + _("There are {} collection films in this year:").format(len(dict_years[year])) + "\\par\n"
                bd=bd + "\\vspace{0.5cm}\n"

                for fi in dict_years[year]:
                    bd=bd + fi.covers.tex_tabular()
            bd=bd +"\n\\newpage\n\n"

            


        print (_("  - Films without year list"))
        if len(films_without_year)>0:
            bd=bd + "\section{"+_("Films without year") +"}\n"
            bd = bd + _("There are {} collection films without year.").format(len(films_without_year)) + "\\par\n"
            for fi in films_without_year:
                bd=bd + fi.covers.tex_tabular()
            bd=bd +"\\newpage\n\n"

        print (_("  - Duplicated films list"))
        duplicated=films_duplicated(qs_films_all)
        if len(duplicated)>0:
            bd=bd + "\section{"+_("Duplicated films") +"}\n"
            bd = bd + _("There are {} collection films duplicated.").format(len(duplicated)) + "\\par\n"
            for fi in duplicated:
                bd=bd + fi.covers.tex_tabular()
            bd=bd +"\\newpage\n\n"


        footer=" \
        \end{document} \
        "

        doc = header + bd + footer

        d=open(f"{tmpdirname}/mymoviebook.tex","w")
        d.write(doc)
        d.close()

        system(f"cd {tmpdirname};pdflatex {tmpdirname}/mymoviebook.tex;  &>/dev/null;pdflatex {tmpdirname}/mymoviebook.tex; pdflatex {tmpdirname}/mymoviebook.tex")
        for output in mem.args.report:
            system(f"cp {tmpdirname}/mymoviebook.pdf {output}")
        
        if mem.args.debug is True:
            show_queries_function()
