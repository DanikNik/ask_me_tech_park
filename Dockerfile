FROM python:3.7

ADD . .
RUN pip install -U -r requirements.txt
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py fakedata --users 10 --questions 30 --tags 17 --answers 5
ENTRYPOINT python3 manage.py reload_cache && gunicorn ask_me_tech_park.wsgi -b "0.0.0.0"

