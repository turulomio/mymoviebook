#!/bin/bash
MYUSER=${1:-postgres}
MYPORT=${2:-5432}
MYHOST=${3:-127.0.0.1}
DATABASE=${4:-mymoviebook}


echo "Introduzca la contraseña de administrador de postgres"
read -s password

echo "Debe ejecutarse desde el directorio sql"
PGPASSWORD=$password pg_dump --no-privileges -s -U $MYUSER -h $MYHOST -p $MYPORT $DATABASE > mymoviebook.sql
PGPASSWORD=$password pg_dump --no-privileges -a -U $MYUSER -h $MYHOST -p $MYPORT $DATABASE -t globals --insert >> mymoviebook.sql
echo "ALTER SEQUENCE public.covers_seq START WITH 1 RESTART;" >> mymoviebook.sql
echo "ALTER SEQUENCE public.films_seq START WITH 1 RESTART;" >> mymoviebook.sql
