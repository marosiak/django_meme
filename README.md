# django_meme
This is meme website written in django for portfolio purposes

You can test this website on https://meme.maciejrosiak.me
# Requirements

`Python >= 3.7`

`Pip >= 19.1`

# Get started

#### Setup sacret_key.txt
You have to create **sacret_key.txt** file in the project directory,
at the same level as **manage.py** and fill it with your sacret key which should be atleast 50 characters long.

#### Install pipenv
``` shell
pip install pipenv
```

#### Install dependencies and create virtual env
``` shell
pipenv install
```

#### Enter virtual env
``` shell 
pipenv shell
```

#### Make migrations
``` shell 
python manage.py makemigrations
python manage.py migrate
```
#### Run dev server
``` shell
python manage.py runserver
```
**If you want to deploy this project, you should check this out:** https://docs.djangoproject.com/en/2.2/howto/deployment/


