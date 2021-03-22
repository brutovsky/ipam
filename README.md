## Django IPAM project installation guide

1. Clone git repository:
$ git clone https://github.com/brutovsky/ipam

2. Install python virtual environment:
$ cd ipam_project
$ python -m venv venv
$ venv/Scripts/activate.bat

3. Import required python packages from `requirements.txt`:
$ pip install -r ../requirements.txt

4. Run development server:
$ python manage.py runserver

5. Server is now accessible via http://127.0.0.1:8000/
