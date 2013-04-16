
DEBUG = True

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.mysql",
        # DB name or path to database file if using sqlite3.
        "NAME": "hm",
        # Not used with sqlite3.
        "USER": "shoaib",
        # Not used with sqlite3.
        "PASSWORD": "shabi123",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "3306",
    }
}

#hi
