import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = False
    POSTGRES_URL="techconf-postgres-db.postgres.database.azure.com"  #TODO: Update value
    POSTGRES_USER="techconfadmin@techconf-postgres-db" #TODO: Update value
    POSTGRES_PW="P@ssword"   #TODO: Update value
    POSTGRES_DB="techconfdb"   #TODO: Update value
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'LWd2tzlprdGHCIPHTd4tp5SBFgDszm'
    SERVICE_BUS_CONNECTION_STRING ='Endpoint=sb://techconf-notfications.servicebus.windows.net/;SharedAccessKeyName=master;SharedAccessKey=kD6h+vuWxJE4rYpZnWOfqyZ4b/PjQrQWy+bMPMa0e3U=;EntityPath=notificationqueue' #TODO: Update value
    SERVICE_BUS_QUEUE_NAME ='notificationqueue'
    ADMIN_EMAIL_ADDRESS: 'info@techconf.com'
    SENDGRID_API_KEY = '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' #Configuration not required, required SendGrid Account

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False