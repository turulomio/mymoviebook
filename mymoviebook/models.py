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

    def path(self, tmpdir):
        return f"{tmpdir}/{self.films.id}.jpg"

    def extract_to_path(self, tmpdir):
        open(self.path(tmpdir), "wb").write(self.cover)

    ## Includes the cover in latex. Remember that to scape {} in python strings, you need to double them {{}}
    ## Used to add the image and the link
    ## @param width Float with the width of the cover
    ## @param height Float with the height of the cover
    ## @return string
    def tex(self,width,height):
        return  "\\href{{{0}}}{{ \\includegraphics[width={1}cm,height={2}cm]{{{3}.jpg}}}}".format(self.films.name2query_filmaffinity(), width, height, self.films.id)
        
    ## Includes the cover in latex. Remember that to scape {} in python strings, you need to double them {{}}
    ## Used for one  cover in a different paragrahp
    ## @param width Float with the width of the cover
    ## @param height Float with the height of the cover
    ## @param show_name Boolean. If True shows the name and the id_dvd. If False only show id_dvd
    ## @return string
    def tex_tabular(self,width=2,height=2, show_name=True):
        bd=""       
        bd=bd + "\\begin{tabular}{ m{2.2cm} m{13cm} }\n"
        if show_name==True:
            bd=bd + "{0} & {1}. (~\\nameref{{sec:{2}}} )\n".format(self.tex(width, height), string2tex(self.films.title()), self.films.dvd)
        else:
            bd=bd + "{0} & ~\\nameref{{sec:{1}}}\n".format(self.tex(width, height), self.films.dvd)#Reference to DVD page
        bd = bd + "\\end{tabular} \n\n"
        return bd


class Films(models.Model):
    savedate = models.DateField(blank=True, null=True)
    name = models.TextField(blank=True, null=True) #title. year
    dvd = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'films'

    def __str__(self):
        if self.year()==None:
            return self.title()
        else:
            return "{} ({})".format(self.title(), self.year())
            
    def title(self):
        if hasattr(self, "_title"):
            return self._title
        self._parse_name()
        return self._title
        
    def year(self):
        if hasattr(self, "_year"):
            return self._year
        self._parse_name()
        return self._year
        

    ## Returns a tu
    def _parse_name(self):
        arr=self.name.split(". ")
        self._title=self.name
        try:
            self._year=int(arr[len(arr)-1])
            self._title=self.name.replace(". "+arr[len(arr)-1], "")
            if self._year<1850 or self._year>date.today().year:#Must be a film
                self._year=None
        except:
            self._year=None

    ## Returns a Internet url to query this film in filmaffinity.com
    def name2query_filmaffinity(self):
        query={"stext": self.title(),}
        return "https://www.filmaffinity.com/es/search.php?{}".format(urlencode(query))

