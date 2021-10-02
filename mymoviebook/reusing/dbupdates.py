import sys

## Class with DB update system
## To make a schema update you just need to add another if, and set the new self.lastcodeupdate
## AFTER EXECUTING I MUST RUN SQL UPDATE SCRIPT TO UPDATE FUTURE INSTALLATIONS
class UpdateDB:
    def __init__(self, mem):
        self.mem=mem
        self.dbversion=self.get_database_version()
        self.lastcodeupdate=201901030929
        self.need_update()

    ## @return Int with the version or None if globals doesn't exist
    def get_database_version(self):
        # Check if globals exists
        cur=self.mem.con.cursor()
        cur.execute("SELECT to_regclass('public.globals')")
        if cur.fetchone()[0]!="globals":
            cur.close()
            return None

        cur.execute("select value from globals where id=1;")
        resultado=cur.fetchone()['value']
        cur.close()
        return int(resultado)

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
            if self.mem.con.is_superuser():
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
            self.set_database_version(201901030837)

        if self.dbversion<201901030929: #Removes LO
            cur=self.mem.con.cursor()
            cur2=self.mem.con.cursor()
            cur.execute("""CREATE OR REPLACE FUNCTION lo_readall(oid) RETURNS bytea
AS $_$

SELECT loread(q3.fd, q3.filesize + q3.must_exec) FROM
	(SELECT q2.fd, q2.filesize, lo_lseek(q2.fd, 0, 0) AS must_exec FROM
		(SELECT q1.fd, lo_lseek(q1.fd, 0, 2) AS filesize FROM
			(SELECT lo_open($1, 262144) AS fd)
		AS q1)
	AS q2)
AS q3

$_$ LANGUAGE sql STRICT;""")
            cur.execute("CREATE SEQUENCE covers_seq  INCREMENT 1  MINVALUE 1  MAXVALUE 9223372036854775807  START 1  CACHE 1")
            cur.execute("CREATE TABLE public.covers(id integer NOT NULL DEFAULT nextval('covers_seq'::regclass), films_id integer, cover bytea, CONSTRAINT covers_pk PRIMARY KEY (id)) WITH (OIDS=FALSE)")
            cur.execute("Select * from films;")
            for row in cur:
                cur2.execute("insert into covers(films_id,cover) values(%s, lo_readall(%s))", (row['id_films'], row['foto']))
            cur.execute("alter table films drop column foto;")      #SHOURLD RUN vacuumlo -U postgres mymoviebook in a console to delete orphaned large objects
            cur.close()
            cur2.close()
            self.set_database_version(201901030929)
        self.mem.con.commit()
        print ("**** Database already updated")
