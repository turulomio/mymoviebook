from decouple import AutoConfig
from dj_database_url import parse as db_url
from os import path, makedirs
from platformdirs import user_config_dir, user_data_dir

## This file uses django-decouple and dj-database-url projects

BASE_DIR = path.dirname(path.abspath(__file__))

#Search for fileconfig and create it if it doesn't exist
FILECONFIG=f"{user_config_dir('mymoviebook')}/settings.ini"
makedirs(path.dirname(FILECONFIG), exist_ok=True)

data_dir=user_data_dir("mymoviebook")
makedirs(data_dir, exist_ok=True)

if not path.exists(FILECONFIG):
    with open(FILECONFIG, "w") as f:
        f.write(f"""[settings]
DEBUG = False
DATABASE_URL = sqlite:///{data_dir}/mymoviebook.db
""")

config = AutoConfig(search_path=FILECONFIG)
db=db_url(config("DATABASE_URL"), conn_max_age=600, conn_health_checks=True)
# Database is defined using parse (db_url) from dj_database_url project
DATABASES = {
    'default': db, 
}

#Since we only have one app which we use
INSTALLED_APPS = (
    'mymoviebook',
)

DEFAULT_AUTO_FIELD ='django.db.models.BigAutoField'

DEBUG=config("DEBUG", default=False,  cast=bool) #To see connection.queries



