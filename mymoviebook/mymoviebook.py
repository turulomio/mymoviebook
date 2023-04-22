from mymoviebook.mem import Mem
from os import environ
from datetime import datetime, date
from glob import glob
from mymoviebook.reusing.libmanagers import ObjectManager_With_Id
from mymoviebook.reusing.text_inputs import input_YN
from mymoviebook import __version__
from os import system, getcwd, path
from pkg_resources import resource_filename

### MAIN SCRIPT ###
def main(parameters=None):
    environ.setdefault("DJANGO_SETTINGS_MODULE", "mymoviebook.settings")

    #instantiate a web sv for django which is a wsgi
    from django.core.wsgi import get_wsgi_application
    get_wsgi_application()

    from mymoviebook import models
    #import your models schema
    print(models.Films.objects.count())

#
    mem=Mem()
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

class FilmManager(ObjectManager_With_Id):
    def __init__(self, mem):
        ObjectManager_With_Id.__init__(self)
        self.mem=mem

    def extract_photos(self):
        for f in self.arr:
            f.cover_db2file()

    def generate_pdf(self):
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
        header = header + "\\usepackage[bookmarksnumbered, colorlinks=true, urlcolor=blue, linkcolor=blue, pdftitle={"+ self.mem._("My movie book") +"}, pdfauthor={MyMovieBook-"+ __version__ +"}, pdfkeywords={movie book}]{hyperref}\n"
        header = header + "\\geometry{verbose,a4paper}\n"
        header = header + "\\usepackage{anysize}\n"
        header = header + "\\marginsize{1.5cm}{1.5cm}{0.5cm}{1cm} \n"
        header = header + "\\usepackage{array}\n"
        header = header + "\\begin{document}\n"
        header = header + "\\title{\\textbf{" + self.mem._("My movie book") + "}}\n"
        header = header + "\\author{MyMovieBook-"+ __version__ +"}\n"

        header = header + "\\setlength{\\parindent}{1cm}\n"
        header = header + "\\setlength{\\parskip}{0.2cm}\n"


        bd=""
        bd=bd + "\\maketitle\n"
        bd=bd + "\\addcontentsline{toc}{section}{"+ self.mem._("Title") +"}\n"

        bd=bd + "\\begin{center}\n"
        bd=bd + "\\includegraphics[width=3cm,height=3cm]{{{0}}}\n".format(icon)
        bd=bd + "\\end{center}\n"
        bd=bd + "\\par\n"
        bd=bd + "\\vspace{1cm}\n"

        bd=bd + self.mem._("This movie book has been generated using version {} of MyMovieBook.").format(__version__) +" " + self.mem._("It's an opensource application published under GPL-3 license.") + "\\par\n"
        bd=bd + self.mem._("The main page of the project is in \href{https://github.com/turulomio/mymoviebook}{GitHub}.")+ "\\par\n"
        bd=bd + self.mem._("This book has {} movies and it was generated at {}.").format(self.length(), datetime.now().time()) +"\\par\n"
        bd=bd + self.mem._("If you make click over a film cover, you'll be redirected to FilmAffinity portal to try to get information of the movie.")
        bd=bd +"\\newpage\n"

        print ("  - " + self.mem._("List by index"))
        bd = bd + "\section{"+ self.mem._("Big covers") +"}\n"
        bd = bd + "\\setlength{\\parindent}{0cm}\n"
        for id_dvd in reversed(self.distinct_id_dvd()):
            bd=bd + "\\subsection*{"+ self.mem._("Index") + " " + str(id_dvd)+"}\n" 
            bd=bd + "\\label{{sec:{0}}}\n".format(id_dvd)
            bd=bd + "\\addcontentsline{toc}{subsection}{"+ self.mem._("Index") + " " + str(id_dvd)+"}\n" 
            
            bd=bd + "\\begin{center}\n"
            bd=bd + "\\begin{tabular}{c c}\n"
            for i, fi in enumerate(self.films_in_id_dvd(id_dvd).arr):
                bd=bd+ "\\begin{tabular}{p{8cm}}\n" #Tabla foto name interior
                bd=bd+ fi.tex_cover(8,6.8) + "\\\\\n"
                bd=bd+ string2tex(fi) +"\\\\\n"
                bd=bd+ "\\end{tabular} &"
                if i % 2==1:
                    bd=bd[:-2]+"\\\\\n"
            bd = bd + "\\end{tabular}\n"
            bd=bd + "\\end{center}\n"
            bd=bd +"\n\\newpage\n\n"


        print (self.mem._("  - Films list with small covers"))
        bd = bd + "\\setlength{\\parindent}{0cm}\n"
        bd=bd + "\section{"+ self.mem._("Small covers") +"}\n"
        for id_dvd in reversed(self.distinct_id_dvd()):
            bd=bd + "\\begin{tabular}{m{2cm} m{2cm} m{2cm} m{2cm} m{2cm} m{2cm} m{2cm}}\n"
            bd=bd + self.mem._("Index") + " " +str(id_dvd) + " & "
            for fi in self.films_in_id_dvd(id_dvd).arr:
                bd=bd + fi.tex_cover(2,2) + " &" 
            bd = bd[:-2]  + "\n"
            bd = bd + "\\end{tabular} \n\n"
        bd=bd +"\n\\newpage\n\n"

        print (self.mem._("  - Films list ordered by title"))
        bd=bd + "\section{"+self.mem._("Order by movie title") +"}\n"
        self.order_by_name()
        for f in self.arr:
            bd=bd + "\\subsection*{"+ string2tex(f) + "} \n"
            bd=bd + "\\addcontentsline{{toc}}{{subsection}}{{{0}}}\n".format(string2tex(f))
            bd=bd + f.tex_cover_tabular(show_name=False)
        bd=bd +"\\newpage\n\n"

        print ("  - Ordered by year films list")
        bd = bd + "\\setlength{\\parindent}{1cm}\n"
        bd=bd + "\section{"+ self.mem._("Order by movie year") + "}\n"
        for year in self.distinct_years():
            if year!="None":
                bd=bd + "\\subsection*{"+ self.mem._("Year") + " " + year +"}\n" 
                bd=bd + "\\addcontentsline{toc}{subsection}{" + self.mem._("Year") + " " + year + "}\n" 
                year_films=self.films_in_year(year)
                if year_films.length()==1:
                    bd = bd + self.mem._("There is only one collection film in this year:") + "\\par\n"
                elif year_films.length()>1:
                    bd = bd + self.mem._("There are {} collection films in this year:").format(year_films.length()) + "\\par\n"
                bd=bd + "\\vspace{0.5cm}\n"

                for fi in year_films.arr:
                    bd=bd + fi.tex_cover_tabular()
            bd=bd +"\n\\newpage\n\n"



        print (self.mem._("  - Films without year list"))
        withoutyear=self.films_without_year()
        if withoutyear.length()>0:
            bd=bd + "\section{"+self.mem._("Films without year") +"}\n"
            bd = bd + self.mem._("There are {} collection films without year.").format(withoutyear.length()) + "\\par\n"
            for fi in withoutyear.arr:
                bd=bd + fi.tex_cover_tabular()
            bd=bd +"\\newpage\n\n"

        print (self.mem._("  - Duplicated films list"))
        duplicated=self.films_duplicated()
        if duplicated.length()>0:
            bd=bd + "\section{"+self.mem._("Duplicated films") +"}\n"
            bd = bd + self.mem._("There are {} collection films duplicated.").format(duplicated.length()) + "\\par\n"
            for fi in duplicated.arr:
                bd=bd + fi.tex_cover_tabular()
            bd=bd +"\\newpage\n\n"


        footer=" \
        \end{document} \
        "

        doc = header + bd + footer

        d=open("/tmp/mymoviebook/mymoviebook.tex","w")
        d.write(doc)
        d.close()

        system("cd /tmp/mymoviebook;pdflatex /tmp/mymoviebook/mymoviebook.tex;  &>/dev/null;pdflatex /tmp/mymoviebook/mymoviebook.tex; pdflatex /tmp/mymoviebook/mymoviebook.tex")
        for output in self.mem.args.report:
            system("cp /tmp/mymoviebook/mymoviebook.pdf {}".format(output))

    def delete_all_films(self):
        for f in self.arr:
            f.delete()
        
    ## Returns a setfilms with the films without year
    def films_without_year(self):        
        result=FilmManager(self.mem)
        for f in self.arr:
            if f.year()==None:
                result.append(f)
        result.order_by_name()
        return result

    ## Returns a FilmManager with the films duplicated in the database
    def films_duplicated(self):
        self.order_by_name()
        result=FilmManager(self.mem)
        last=None
        for f in self.arr:
            if last!=None and f.name()==last.name() and f.year()==last.year():
                result.append(f)
                result.append(last)
            last=f
        return result

    def distinct_id_dvd(self):
        """Returns a ordered list with distinct id_dvd in the set"""
        s=set([])
        for f in self.arr:
            s.add(f.id_dvd)
        l=list(s)
        return sorted(l)

    def distinct_years(self):
        """Returns a ordered list with distinct id_dvd in the set"""
        s=set([])
        for f in self.arr:
            s.add(str(f.year()))#String para añadir None
        l=list(s)
        return sorted(l)

    def films_in_id_dvd(self, id_dvd):
        """Returns a FilmManager with the films in a dvd and sorts them by name"""
        result=FilmManager(self.mem)
        for f in self.arr:
            if f.id_dvd==id_dvd:
                result.arr.append(f)
        result.order_by_name()
        return result

    def films_in_year(self, year):
        """Return a FilmManager with the filmns in a year and sorts them by name"""
        result=FilmManager(self.mem)
        for f in self.arr:
            if str(f.year())==year:
                result.append(f)
        result.order_by_name()
        return result
        
    def order_by_name(self):
        try:
            self.arr=sorted(self.arr, key=lambda c: c.name(),  reverse=False)       
            return True
        except:
            return False        
        
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
