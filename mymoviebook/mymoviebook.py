import os, sys, glob, datetime, psycopg2, psycopg2.extras, shutil
import pkg_resources
import argparse
import getpass
import gettext
from mymoviebook.version import __version__, __versiondate__
from officegenerator import ODT_Standard
from mymoviebook.dbupdates import UpdateDB
from mymoviebook.connection_pg import Connection
from mymoviebook.libmanagers import ObjectManager_With_IdName

try:
    t=gettext.translation('mymoviebook',pkg_resources.resource_filename("mymoviebook","locale"))
    _=t.gettext
except:
    _=str


class Mem:
    def __init__(self):
        self.con=Connection()

class Film:
    def __init__(self, mem):
        self.mem=mem
        self.id=None
        self.savedate=None
        self.name=None
        self.coverpath=None
        self.id_dvd=None
        self.year=None

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

    ## Converts the film name to a list without rare characters
    def name2list_without_rare_characters(self):
        #Removes special chars
        name=""
        for letter in self.name.lower():
            if letter not in ",.;()[]:":
                name=name+letter

        #Replace special char
        name=name.replace("á","a")
        name=name.replace("é","e")
        name=name.replace("í","i")
        name=name.replace("ó","o")
        name=name.replace("ú","u")
        name=name.replace("ñ","ñ")

        r=[]
        for word in name.split(" "):
            r.append(word)
        return r

    ## Returns a Internet url to query this film in sensacine.com
    def name2query_sensacine(self):
        r=""
        for word in self.name2list_without_rare_characters():
            r=r+word + "+"
        return "http://www.sensacine.com/busqueda/?q={}".format(r[:-1])

    ## Returns a Internet url to query this film in filmaffinity.com
    def name2query_filmaffinity(self):
        r=""
        for word in self.name2list_without_rare_characters():
            r=r+word + "+"
        return "https://www.filmaffinity.com/es/search.php?stext={}".format(r[:-1])

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
    ## @param width Float with the width of the cover
    ## @param height Float with the height of the cover
    ## @return string
    def tex_cover(self,width,height):
        return  "\\href{{{0}}}{{ \\includegraphics[width={1}cm,height={2}cm]{{{3}.jpg}}}}".format(self.name2query_filmaffinity(), width, height, self.id)

    def save(self):
        if self.id==None:
            if self.year==None:
                name=self.name
            else:
                name="{}. {}".format(self.name,self.year)
            cur=self.mem.con.cursor()
            cur.execute("insert into films (savedate, name, id_dvd) values (%s, %s, %s) returning id_films",(self.savedate, name, self.id_dvd))
            self.id=cur.fetchone()[0]
            bytea=open(self.coverpath, "rb").read()
            cur.execute("insert into covers (films_id, cover) values (%s, %s)",(self.id, bytea))
            cur.close()
            return True

class SetFilms(ObjectManager_With_IdName):
    def __init__(self, mem):
        ObjectManager_With_IdName.__init__(self)
        self.mem=mem

    def extract_photos(self):
        for f in self.arr:
            f.cover_db2file()

    def generate_pdf(self):
        icon=pkg_resources.resource_filename("mymoviebook","images/mymoviebook.png")


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
        header = header + "\\marginsize{1.5cm}{1.5cm}{1.5cm}{1.5cm} \n"
        header = header + "\\usepackage{array}\n"
        header = header + "\\begin{document}\n"
        header = header + "\\title{\\textbf{" + _("My movie book") + "}}\n"

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
        bd=bd + _("This book has {} movies and it was generated at {}.").format(self.length(), datetime.datetime.now().time()) +"\\par\n"
        bd=bd +"\\newpage\n"

        print ("  - " + _("List by index"))
        # LISTADO DE DVD POR PAGINA
        bd = bd + "\section{"+ _("Big covers") +"}\n"
        for id_dvd in reversed(self.distinct_id_dvd()):
            # Son necesarias las dos
            bd=bd + "\\subsection*{"+ _("Index") + " " + str(id_dvd)+"}\n" 
            bd=bd + "\\label{{sec:{0}}}\n".format(id_dvd)
            bd=bd + "\\addcontentsline{toc}{subsection}{"+ _("Index") + " " + str(id_dvd)+"}\n" 
            bd=bd + "\\begin{tabular}{c c}\n"
            for i, fi in enumerate(self.films_in_id_dvd(id_dvd).arr):
                bd=bd+ "\\begin{tabular}{p{7.1cm}}\n" #Tabla foto name interior
                bd=bd+ fi.tex_cover(6.7,6.7) + "\\\\\n"
                bd=bd+ string2tex(fi.name) +"\\\\\n"
                bd=bd+ "\\end{tabular} &"
                if i % 2==1:
                    bd=bd[:-2]+"\\\\\n"
            bd = bd + "\\end{tabular}\n"
            bd=bd +"\n\\newpage\n\n"


        print ("  - Listado de carátulas en pequeño")

        bd = bd + "\\setlength{\\parindent}{0cm}\n"
        # LISTADO DE CARATULAS JUNTAS
        bd=bd + "\section{"+ _("Small covers") +"}\n"
        for id_dvd in reversed(self.distinct_id_dvd()):
            bd=bd + "\\begin{tabular}{m{2.1cm} m{2.1cm} m{2.1cm} m{2.1cm} m{2.1cm} m{2.1cm} m{2.1cm}}\n"
            bd=bd + _("Index") + " " +str(id_dvd) + " & "
            for fi in self.films_in_id_dvd(id_dvd).arr:
                bd=bd + fi.tex_cover(2.1,2.1) + " &" 
            bd = bd[:-2]  + "\\\\\n"
            bd = bd + "\\end{tabular} \\\\\n\n"
        bd=bd +"\n\\newpage\n\n"


        print ("  - Listado ordenado alfabéticamente")
        # ORDENADAS ALFABETICAMENTE
        bd=bd + "\section{"+_("Order by movie title") +"}\n"
        self.order_by_name()
        for f in self.arr:
            bd=bd + "\\subsection*{{{0}}}\n".format(string2tex(f.name))
            bd=bd + "\\addcontentsline{{toc}}{{subsection}}{{{0}}}\n".format(string2tex(f.name))
            bd=bd + "\\begin{tabular}{m{2.3cm} m{15cm}}\n"
            bd=bd + f.tex_cover(2.2,2.2) + " & ~\\nameref{{sec:{0}}}\\\\\n".format(f.id_dvd)#Reference to DVD page
            bd = bd + "\\end{tabular}\n\n"
        bd=bd +"\\newpage\n\n"


        print ("  - Listado ordenado por años")
        # ORDENADAS POR AÑO
        bd=bd + "\section{"+ _("Order by movie year") + "}\n"
        for year in reversed(self.distinct_years()):
            if year=="None":
                bd=bd + "\\subsection*{" + _("Unknown year") + "}\n" 
                bd=bd + "\\addcontentsline{toc}{subsection}{" + _("Unknown year") + "}\n" 
            else:
                bd=bd + "\\subsection*{"+ _("Year") + " " + year +"}\n" 
                bd=bd + "\\addcontentsline{toc}{subsection}{" + _("Year") + " " + year + "}\n" 
            for fi in self.films_in_year(year).arr:
                bd=bd + "\\begin{tabular}{m{2.3cm} m{15cm}}\n"
                bd=bd + "{0} & {1}. (~\\nameref{{sec:{2}}} )\\\\\n".format(fi.tex_cover(2.2,2.2), string2tex(fi.name), fi.id_dvd)
                bd = bd + "\\end{tabular} \\\\\n\n"
            bd=bd +"\n\\newpage\n\n"

        footer=" \
        \end{document} \
        "

        doc = header + bd + footer

        d=open("/tmp/mymoviebook/mymoviebook.tex","w")
        d.write(doc)
        d.close()

        os.system("cd /tmp/mymoviebook;pdflatex /tmp/mymoviebook/mymoviebook.tex;  &>/dev/null;pdflatex /tmp/mymoviebook/mymoviebook.tex; pdflatex /tmp/mymoviebook/mymoviebook.tex")
        for output in args.output:
            os.system("cp /tmp/mymoviebook/mymoviebook.pdf {}".format(output))

    def generate_odt(self):
        odt=ODT_Standard(args.output[0])
        odt.title(_("Movie list"), 1)
        odt.simpleParagraph(_("This list has {} films and was generated at {} with MyMovieBook-{}").format(self.length(), datetime.date.today(), __version__))
        
        #Add photos to document
        for f in self.arr:
            odt.addImage(f.coverpath_in_tmp(), str(f.id))
        
        print ("  - Listado por página")
        odt.header(_("Big covers"), 1)
        for id_dvd in reversed(self.distinct_id_dvd()):
            odt.header(_("Index {}").format(id_dvd), 2)
            for i, fi in enumerate(self.films_in_id_dvd(id_dvd).arr):
                odt.illustration([str(fi.id), ], 3, 3, str(fi.id))
                odt.simpleParagraph(fi.name)
        
        print ("  - Listado de carátulas en pequeño")
        odt.header(_("Small covers"), 1)
        for id_dvd in reversed(self.distinct_id_dvd()):
            odt.simpleParagraph(_("Index {}").format(id_dvd))
            photo_arr=[]
            for fi in self.films_in_id_dvd(id_dvd).arr:
                photo_arr.append(str(fi.id))
            odt.illustration(photo_arr, 3, 3, str(id_dvd))
            
        print ("  - Listado ordenado alfabéticamente")
        odt.header(_("Order by name"), 1)
        self.order_by_name()
        for f in self.arr:
            odt.header(f.name, 2)
            odt.illustration([str(f.id), ], 3, 3, str(f.id))
        
        print ("  - Listado ordenado por años")
        odt.header(_("Order by year"), 1)
        for year in reversed(self.distinct_years()):
            if year=="None":
                odt.header(_("Unknown year"), 2)
            else:
                odt.header(_("Year {}").format(year), 2)
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
        """Returns a SetFilms with the films in a dvd and sorts them by name"""
        result=SetFilms(self.mem)
        for f in self.arr:
            if f.id_dvd==id_dvd:
                result.arr.append(f)
        result.order_by_name()
        return result

    def films_in_year(self, year):
        """Return a SetFilms with the filmns in a year and sorts them by name"""
        result=SetFilms(self.mem)
        for f in self.arr:
            if str(f.year)==year:
                result.append(f)
        result.order_by_name()
        return result

def string2shell(cadena):
    cadena=cadena.replace("'","\\'")
    return cadena

def Yn(pregunta):
    while True:
        user_input = input(pregunta +" [Y|n]").strip().lower()
        if not user_input or user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            print ("Please enter 'Y', 'n'")

def string2tex(cadena):
    cadena=cadena.replace('[','$ [ $')
    cadena=cadena.replace(']','$ ] $')
    cadena=cadena.replace('&','\&')
    cadena=cadena.replace('²','$ ^2 $')
    cadena=cadena.replace('#', '\#')
    return cadena


### MAIN SCRIPT ###
def main(parameters=None):
    parser=argparse.ArgumentParser(prog='mymoviebook', description=_('Generate your personal movie collection book'), epilog=_("Developed by Mariano Muñoz 2012-{}".format(__versiondate__.year)), formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--version', action='version', version=__version__)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--insert', help=_('Insert films from current numbered directory'), action="store_true")
    group.add_argument('--generate', help=_('Generate films documentation'), action="store_true")

    group_db=parser.add_argument_group(_("Postgres database connection parameters"))
    group_db.add_argument('--user', help=_('Postgresql user'), default='postgres')
    group_db.add_argument('--port', help=_('Postgresql server port'), default=5432)
    group_db.add_argument('--server', help=_('Postgresql server address'), default='127.0.0.1')
    group_db.add_argument('--db', help=_('Postgresql database'), default='mymoviebook')

    group_generate=parser.add_argument_group(_("Generate command parameters"))
    group_generate.add_argument('--output', help=_("Path to the output document"), action="append", default=[])
    group_generate.add_argument('--format', help=_("select output format. Default is PDF"), action="store", choices=['PDF', 'ODT'],  default='PDF')

    global args
    args=parser.parse_args(parameters)

    mem=Mem()

    mem.con.user=args.user
    mem.con.server=args.server
    mem.con.port=args.port
    mem.con.db=args.db

    print(_("Write the password for {}").format(mem.con.url_string()))
    mem.con.password=getpass.getpass()
    mem.con.connect()

    UpdateDB(mem)

    cwd=os.getcwd().split("/")
    try:
        shutil.rmtree("/tmp/mymoviebook")
    except:
        pass
    os.mkdir("/tmp/mymoviebook")
    os.system("chmod 777 /tmp/mymoviebook")


    if args.insert==True:# insertar
        try:
            id=int(cwd[len(cwd)-1])
        except:
            print (_("Current directory is not numeric"))
            sys.exit(100)

        if Yn("El identificador del dispositivo a introducir es '" +str(id) + "'. ¿Desea continuar?")==False:
            sys.exit(100)


        print ("+ Comprobando que el nombre de los videos y las imágenes tienen el formato correcto")
        for file in glob.glob( os.getcwd()+ "/*.jpg" ):
            if os.path.exists(file[:-3]+"avi")==False and os.path.exists(file[:-3]+"mpg")==False and os.path.exists(file[:-3]+"mkv")==False:
                print ("No existe un video con el mismo nombre '" +  file[:-3]+"'")
                sys.exit(100)

        sf=SetFilms(mem)
        sf.load("SELECT id_films, savedate, name, id_dvd, cover FROM films, covers WHERE covers.films_id=films.id_films and id_dvd=" + str(id))

        # "Chequeando si hay registros en la base de datos del dispositivo " + str(id)
        if len(sf.arr)>0:
            if Yn("+ ¿Desea borrar los registros del dispositivo '" +str(id) + "'?")==False:
                sys.exit(100)
            else:
                print ("   - Borrando los registros...")
                sf.delete_all_films()
        global cur
        cur=mem.con.cursor()
        print ("+ Insertando las peliculas en la base de datos")
        for file in glob.glob( os.getcwd()+ "/*.jpg" ):
            f=Film(mem).init__create(datetime.date.today(), file[len(os.getcwd())+1:-4], file,id)
            f.save()
            print ("    - {0}".format(file[len(os.getcwd())+1:-4]))
        cur.close()
        mem.con.commit()

    elif args.generate==True:
        # SACA LAS IMÁGENES DE LA BASE DE DATOS
        print ("  - Sacando las imágenes")
        if len(args.output)==0:
            print ("    Necesita añadir al menos un documento de salida. Por ejemplo '--output mymoviebook.pdf'")
            sys.exit(0)
        sf=SetFilms(mem)
        sf.load("SELECT * FROM films")
        sf.extract_photos()
        if args.format=="PDF":
            sf.generate_pdf()
        else:
            sf.generate_odt()
    else:
        parser.print_help()

    mem.con.disconnect()

    shutil.rmtree("/tmp/mymoviebook")
