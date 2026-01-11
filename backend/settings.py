DATABASES = {
    'default': {
        'ENGINE' : 'mssql',
        'NAME': 'UTH_CONFMS',
        'USER': 'sa',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    }
}