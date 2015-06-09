# SchPark - Web Scheduler for Spark
SchPark is a Scheduler for Spark with a web interface for manage all jobs. It uses spark-submit program for send jobs to Spark Master.

## 1. Requeriments

- Django 1.8
- django-cron https://github.com/Tivix/django-cron
- Apache Spark

## 2. Installation example on Debian

    git clone https://github.com/trencube/SchPark.git
    cd SchPark
    sudo python manage.py collectstatic
    sudo chown -R www-data:www-data *


## 3. Configuration

#### Config variables in SchPark/settings.py
SPARK_BIN_DIR = '/opt/spark/bin' </br>
Is the spark binary directory

SPARK_MASTER = '127.0.0.1:7077' </br>
Is the ip and port of spark master


#### Vhost example for apache
    <VirtualHost *:80>

        ServerName serverdomain.com
        WSGIScriptAlias / /var/www/SchPark/SchPark/wsgi.py

        Alias /static/ /var/www/SchPark/static/

        <Directory />
                Options FollowSymLinks
                AllowOverride None
                Order deny,allow
                Allow from all
        </Directory>

    </VirtualHost>
