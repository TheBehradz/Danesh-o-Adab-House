def get_django_config() :
    return {
        'DATABASES' : {
            'default': {
            'ENGINE': 'django.db.backends.mysql', 
            'NAME': 'database name here',
            'USER': 'database username here',
            'OPTIONS': {'charset': 'utf8mb4'},
            'PASSWORD': 'v8+eZ{qhkE/b',
            'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
            'PORT': '3306',
            'CONN_MAX_AGE': None,}},
        'INSTALLED_APPS' : [
            'mand_base.mandapp'],
        'TIME_ZONE' : 'Asia/Tehran',
        'USE_I18N' : True,
        'USE_L10N' : True,
        'USE_TZ' : True,
    }