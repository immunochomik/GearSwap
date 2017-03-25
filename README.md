
## Set up and activate virtual environment

```bash
virtualenv testEvn
. testEvn/bin/activate
```

## Install requirements migrate and run dev server

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

