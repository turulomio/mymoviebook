import sys

## Class with DB update system
## To make a schema update you just need to add another if, and set the new self.lastcodeupdate
## AFTER EXECUTING I MUST RUN SQL UPDATE SCRIPT TO UPDATE FUTURE INSTALLATIONS
class UpdateDB:
    def __init__(self, mem):
        self.mem=mem
        self.dbversion=self.get_database_version()
        self.lastcodeupdate=201909030837
        self.need_update()

    ## @return Int with the version or None if globals doesn't exist
    def get_database_version(self):
        # Check if globals exists
        cur=self.mem.con.cursor()
        cur.execute("SELECT to_regclass('public.globals')")
        if cur.fetchone()[0]!="globals":
            cur.close()
            return None

        cur.execute("select value from globals where id_globals=1;")
        resultado=cur.fetchone()['value']
        cur.close()
        self.dbversion=int(resultado)

    def set_database_version(self, valor):
        print("**** Updating database from {} to {}".format(self.dbversion, valor))
        cur=self.mem.con.cursor()
        if self.dbversion==None:
            cur.execute("insert into globals (id,global,value) values (%s,%s,%s);", (1,"Version", valor ))
        else:
            cur.execute("update globals set global=%s, value=%s where id=1;", ("Version", valor ))
        cur.close()
        self.dbversion=valor

    def need_update(self):
        if self.dbversion==None or self.dbversion<self.lastcodeupdate:
            if self.mem.is_superuser():
                self.run()
            else:
                print(_("MyMovieBook database needs to be updated. Please login with a superuser role."))
                sys.exit(2)
        elif self.dbversion>self.lastcodeupdate:
            print(_("MyMovieBook app is older than database. Please update it."))
            sys.exit(3)
        elif self.dbversion==self.lastcodeupdate:
            return

    def run(self): 
        if self.dbversion==None:
            cur=self.mem.con.cursor()
            cur.execute("CREATE TABLE public.globals (id integer NOT NULL, global text, value text)")
            cur.execute("ALTER TABLE ONLY public.globals ADD CONSTRAINT pk_globals PRIMARY KEY (id)")
            cur.close()
            self.set_database_version(201909030837)


        self.mem.con.commit()
        print ("**** Database already updated")
