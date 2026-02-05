from .base_setting import *



DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'conference',
        'USER': 'sa',
        'PASSWORD': '123456',
        'HOST': 'LAPTOP-6R6QNJFA\\MSSQLSERVER1',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'TrustServerCertificate': 'yes',
        },
    }
}
