# django_test
Django exchange rates test project

Installing guide:

Python3 is required

Install requirements:
pip install -r requirements.txt 

Install postgres

Setup the database:
psql postgres
CREATE DATABASE currency;
CREATE USER alex WITH PASSWORD '4iHgvRPA';
GRANT ALL PRIVILEGES ON DATABASE currency TO alex;
ALTER USER alex CREATEDB;

Setup and start redis:
brew install redis
brew services start redis

Create database for django:
python3 manage.py migrate

Run:
python3 manager.py runserver --noreload

Tests:
python3 manager.py test currency



