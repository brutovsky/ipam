## Django IPAM project installation guide

1. Clone git repository:
$ git clone https://github.com/brutovsky/ipam

2. Install python virtual environment:  
$ cd ipam_project  
$ python -m venv venv  
$ venv/Scripts/activate.bat

3. Import required python packages from `requirements.txt`:  
$ pip install -r ../requirements.txt

4. Create PostgreSQL database:
$ psql -U postgres  
postgres=# CREATE DATABASE ipam;  
postgres=# \q

5. Modify (if needed) 'settings.py' file from 'ipam_project' directory:  

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ipam',
        'USER': 'postgres',
        'PASSWORD': 'your-pass',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

6. Create superadmin in django project:  
$ python manage.py migrate auth  
$ python manage.py migrate  
$ python manage.py createsuperuser --email admin@example.com --username admin

7. Run development server:  
$ python manage.py runserver

8. Server is now accessible via http://127.0.0.1:8000/

9. Access admin page via http://127.0.0.1:8000/admin

10. Access REST api via http://127.0.0.1:8000/api
