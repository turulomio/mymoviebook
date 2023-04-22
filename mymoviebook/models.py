# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from datetime import date
from django.db import models
from mymoviebook.reusing.casts import string2tex
from urllib.parse import urlencode


class Covers(models.Model):  
    films = models.OneToOneField("Films", on_delete=models.CASCADE, blank=False, null=False, primary_key=True)
    cover = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'covers'


class Films(models.Model):
    savedate = models.DateField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    dvd = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'films'

    def __repr__(self):
        name, year=self.__parse_rawname()
        if year==None:
            return name
        else:
            return "{} ({})".format(name, year)

    ## Returns a tu
    def __parse_rawname(self):
        arr=self.rawname.split(". ")
        name=self.rawname
        try:
            year=int(arr[len(arr)-1])
            name=self.rawname.replace(". "+arr[len(arr)-1], "")
            if year<1850 or year>date.today().year:#Must be a film
                year=None
        except:
            year=None
        return (name, year)
        
    ## Returns Film year integer or None
    def year(self):
        return self.__parse_rawname()[1]

    ## Returns Film name
    def name(self):
        return self.__parse_rawname()[0]

    ## Returns a Internet url to query this film in sensacine.com
    def name2query_sensacine(self):
        query={"q": self.name(),}
        return "http://www.sensacine.com/busqueda/?{}".format(urlencode(query))

    ## Returns a Internet url to query this film in filmaffinity.com
    def name2query_filmaffinity(self):
        query={"stext": self.name(),}
        return "https://www.filmaffinity.com/es/search.php?{}".format(urlencode(query))

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
    def tex_cover_tabular(self,width=2,height=2, show_name=True):
        bd=""       
        bd=bd + "\\begin{tabular}{ m{2.2cm} m{13cm} }\n"
        if show_name==True:
            bd=bd + "{0} & {1}. (~\\nameref{{sec:{2}}} )\n".format(self.tex_cover(width, height), string2tex(self.name()), self.id_dvd)
        else:
            bd=bd + "{0} & ~\\nameref{{sec:{1}}}\n".format(self.tex_cover(width, height), self.id_dvd)#Reference to DVD page
        bd = bd + "\\end{tabular} \n\n"
        return bd

