from datetime import datetime, date
from glob import glob
from mymoviebook.casts import string2tex
from mymoviebook.libmanagers import ObjectManager_With_IdName
from mymoviebook.text_inputs import input_YN
from mymoviebook.version import __version__
from officegenerator import ODT_Standard
from os import system, getcwd, path
from pkg_resources import resource_filename
from urllib.parse import urlencode

class Film:
    def __init__(self, mem):
        self.mem=mem
        self.id=None
        self.savedate=None
        self.name=None
        self.coverpath=None
        self.id_dvd=None
        self.year=None

    def __repr__(self):
        if self.year==None:
            return self.name
        else:
            return "{} ({})".format(self.name, self.year)

    def init__create(self,savedate, name, coverpath, id_dvd):
        """Introduce pathcover, ya que debera luego hacer un insert, id siempre es None, year es None, pero lo parsea en la funcion"""
        self.savedate=savedate
        self.name=name
        self.coverpath=coverpath
        self.id_dvd=id_dvd
        self.parse_name()
        return self

    def init__from_db(self,row):
        self.id=row['id_films']
        self.savedate=row['savedate']
        self.name=row['name']
        self.id_dvd=row['id_dvd']
        self.parse_name()
        return self

    def parse_name(self):
        name=self.name
        arr=name.split(". ")
        try:
            self.year=int(arr[len(arr)-1])
            self.name=name.replace(". "+arr[len(arr)-1], "")
            if self.year<1850 or self.year>datetime.date.today().year:#Must be a film
                self.year=None
        except:
            self.year=None

    ## Returns a Internet url to query this film in sensacine.com
    def name2query_sensacine(self):
        query={"q": self.name,}
        return "http://www.sensacine.com/busqueda/?{}".format(urlencode(query))

    ## Returns a Internet url to query this film in filmaffinity.com
    def name2query_filmaffinity(self):
        query={"stext": self.name,}
        return "https://www.filmaffinity.com/es/search.php?{}".format(urlencode(query))

    def delete(self):
        cur=self.mem.con.cursor()
        sqldel="delete from films where id_films=" + str(self.id)
        cur.execute(sqldel)
        sqldel="delete from covers where films_id=" + str(self.id)
        cur.execute(sqldel)
        cur.close()


    def cover_db2file(self):
        cur=self.mem.con.cursor()
        cur.execute("SELECT cover FROM covers where films_id=%s", (self.id, ))#Si es null peta el open, mejor que devuelva fals3ee3 que pasar a variable
        if cur.rowcount==1:
            open(self.coverpath_in_tmp(), "wb").write(cur.fetchone()[0])
            cur.close()
            return True
        cur.close()
        return False

    ## Path to cover in /tmp directory
    def coverpath_in_tmp(self):
        return '/tmp/mymoviebook/{}.jpg'.format(self.id)

    ## Includes the cover in latex. Remember that to scape {} in python strings, you need to double them {{}}
    ## Used to add the image and the link
    ## @param width Float with the width of the cover
    ## @param height Float with the height of the cover
    ## @return string
    def tex_cover(self,width,height):
        return  "\\href{{{0}}}{{ \\includegraphics[width={1}cm,height={2}cm]{{{3}.jpg}}}}".format(self.name2query_filmaffinity(), width, height, self.id)
        
    ## Includes the cover in latex. Remember that to scape {} in python strings, you need to double them {{}}
    ## Used for one  cover in a different paragrahp
    ## @param width Float with the width of the cover
    ## @param height Float with the height of the cover
    ## @param show_name Boolean. If True shows the name and the id_dvd. If False only show id_dvd
    ## @return string
    def tex_cover_tabular(self,width=2.2,height=2.2, show_name=True):
        bd=""       
        bd=bd + "\\begin{tabular}{m{2.3cm} m{15cm}}\n"
        if show_name==True:
            bd=bd + "{0} & {1}. (~\\nameref{{sec:{2}}} )\\\\\n".format(self.tex_cover(width, height), string2tex(self.name), self.id_dvd)
        else:
            bd=bd + "{0} & ~\\nameref{{sec:{1}}}\\\\\n".format(self.tex_cover(width, height), self.id_dvd)#Reference to DVD page
        bd = bd + "\\end{tabular} \\\\\n\n"
        return bd

    def save(self):
        if self.id==None:
            if self.year==None:
                name=self.name
            else:
                name="{}. {}".format(self.name,self.year)
            self.id=self.mem.con.cursor_one_field("insert into films (savedate, name, id_dvd) values (%s, %s, %s) returning id_films",(self.savedate, name, self.id_dvd))
            bytea=open(self.coverpath, "rb").read()
            self.mem.con.execute("insert into covers (films_id, cover) values (%s, %s)",(self.id, bytea))
            return True

class FilmManager(ObjectManager_With_IdName):
    def __init__(self, mem):
        ObjectManager_With_IdName.__init__(self)
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
        header = header + "\\marginsize{1.5cm}{1.5cm}{1.5cm}{1.5cm} \n"
        header = header + "\\usepackage{array}\n"
        header = header + "\\begin{document}\n"
        header = header + "\\title{\\textbf{" + self.mem._("My movie book") + "}}\n"

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
        for id_dvd in reversed(self.distinct_id_dvd()):
            bd=bd + "\\subsection*{"+ self.mem._("Index") + " " + str(id_dvd)+"}\n" 
            bd=bd + "\\label{{sec:{0}}}\n".format(id_dvd)
            bd=bd + "\\addcontentsline{toc}{subsection}{"+ self.mem._("Index") + " " + str(id_dvd)+"}\n" 
            bd=bd + "\\begin{tabular}{c c}\n"
            for i, fi in enumerate(self.films_in_id_dvd(id_dvd).arr):
                bd=bd+ "\\begin{tabular}{p{7.1cm}}\n" #Tabla foto name interior
                bd=bd+ fi.tex_cover(6.7,6.7) + "\\\\\n"
                bd=bd+ string2tex(fi) +"\\\\\n"
                bd=bd+ "\\end{tabular} &"
                if i % 2==1:
                    bd=bd[:-2]+"\\\\\n"
            bd = bd + "\\end{tabular}\n"
            bd=bd +"\n\\newpage\n\n"


        print (self.mem._("  - Films list with small covers"))

        bd = bd + "\\setlength{\\parindent}{0cm}\n"
        bd=bd + "\section{"+ self.mem._("Small covers") +"}\n"
        for id_dvd in reversed(self.distinct_id_dvd()):
            bd=bd + "\\begin{tabular}{m{2.1cm} m{2.1cm} m{2.1cm} m{2.1cm} m{2.1cm} m{2.1cm} m{2.1cm}}\n"
            bd=bd + self.mem._("Index") + " " +str(id_dvd) + " & "
            for fi in self.films_in_id_dvd(id_dvd).arr:
                bd=bd + fi.tex_cover(2.1,2.1) + " &" 
            bd = bd[:-2]  + "\\\\\n"
            bd = bd + "\\end{tabular} \\\\\n\n"
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

    def generate_odt(self):
        odt=ODT_Standard(self.mem.args.output[0])
        odt.title(self.mem._("Movie list"), 1)
        odt.simpleParagraph(self.mem._("This list has {} films and was generated at {} with MyMovieBook-{}").format(self.length(), date.today(), __version__))
        
        #Add photos to document
        for f in self.arr:
            odt.addImage(f.coverpath_in_tmp(), str(f.id))
        
        print ("  - Listado por página")
        odt.header(self.mem._("Big covers"), 1)
        for id_dvd in reversed(self.distinct_id_dvd()):
            odt.header(self.mem._("Index {}").format(id_dvd), 2)
            for i, fi in enumerate(self.films_in_id_dvd(id_dvd).arr):
                odt.illustration([str(fi.id), ], 3, 3, str(fi.id))
                odt.simpleParagraph(fi.name)
        
        print ("  - Listado de carátulas en pequeño")
        odt.header(self.mem._("Small covers"), 1)
        for id_dvd in reversed(self.distinct_id_dvd()):
            odt.simpleParagraph(self.mem._("Index {}").format(id_dvd))
            photo_arr=[]
            for fi in self.films_in_id_dvd(id_dvd).arr:
                photo_arr.append(str(fi.id))
            odt.illustration(photo_arr, 3, 3, str(id_dvd))
            
        print ("  - Listado ordenado alfabéticamente")
        odt.header(self.mem._("Order by name"), 1)
        self.order_by_name()
        for f in self.arr:
            odt.header(f.name, 2)
            odt.illustration([str(f.id), ], 3, 3, str(f.id))
        
        print ("  - Listado ordenado por años")
        odt.header(self.mem._("Order by year"), 1)
        for year in self.distinct_years():
            if year=="None":
                odt.header(self.mem._("Unknown year"), 2)
            else:
                odt.header(self.mem._("Year {}").format(year), 2)
            for fi in self.films_in_year(year).arr:
                odt.illustration([str(fi.id), ], 3, 3, str(fi.id))

        odt.save()

    def load(self,sql):
        cur=self.mem.con.cursor()
        cur.execute(sql)
        for row in cur:
            self.arr.append(Film(self.mem).init__from_db(row))
        self.mem.con.commit()
        cur.close()

    def delete_all_films(self):
        for f in self.arr:
            f.delete()
        
    ## Returns a setfilms with the films without year
    def films_without_year(self):        
        result=FilmManager(self.mem)
        for f in self.arr:
            if f.year==None:
                result.append(f)
        result.order_by_name()
        return result

    ## Returns a FilmManager with the films duplicated in the database
    def films_duplicated(self):
        self.order_by_name()
        result=FilmManager(self.mem)
        last=None
        for f in self.arr:
            if last!=None and f.name==last.name and f.year==last.year:
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
            s.add(str(f.year))#String para añadir None
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
            if str(f.year)==year:
                result.append(f)
        result.order_by_name()
        return result
        
## Function to add movies to a database from console
def add_movies_to_database(mem):
    try:
        cwd=getcwd().split("/")
        id=int(cwd[len(cwd)-1])
    except:
        print (mem._("Current directory is not numeric"))
        exit(100)

    if input_YN(mem._("The id of the directory to add is '{}'. Do you want to continue?").format(id))==False:
        exit(100)


    print ("+ " + mem._("Checking that the movies have the correct format..."))
    for file in glob( getcwd()+ "/*.jpg" ):
        if path.exists(file[:-3]+"avi")==False and path.exists(file[:-3]+"mpg")==False and path.exists(file[:-3]+"mkv")==False:
            print (mem._("There isn't a movie with the same name '{}'").format(file[:-3]))
            exit(100)

    sf=FilmManager(mem)
    sf.load("SELECT id_films, savedate, name, id_dvd, cover FROM films, covers WHERE covers.films_id=films.id_films and id_dvd=" + str(id))

    # "Chequeando si hay registros en la base de datos del dispositivo " + str(id)
    if len(sf.arr)>0:
        if input_YN("+ " + mem._("Do you want to overwrite the information of directory '{}'?").format(id))==False:
            exit(100)
        else:
            print ("   - " + mem._("Deleting information..."))
            sf.delete_all_films()
            
    print ("+ "+ mem._("Adding movies to the database"))
    for file in glob( getcwd()+ "/*.jpg" ):
        f=Film(mem).init__create(date.today(), file[len(getcwd())+1:-4], file,id)
        f.save()
        print ("    - {0}".format(file[len(getcwd())+1:-4]))
    mem.con.commit()
