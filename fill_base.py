#! venv//bin/python

import sys
import os
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ask_me_tech_park.settings'
django.setup()

print('[+] Set up environment')

from django.contrib.auth.models import User
from questions.models import Question, Tag
from django.contrib.auth.models import User
from faker import Faker
from random import randint

fake = Faker()
admin = User.objects.create_superuser(username='admin', password='admin', email='root@admin.com')
admin.save()
# Person.objects.create(name='ADMIN', surname='ADMIN', nickname='ADMIN', user=admin)
print('[+] Created superuser')

count = 0
for i in range(20):
    try:
        tag = Tag.objects.create(text=fake.word())
        tag.save()
        print('[+] Created tag {}'.format(tag.text))
        count += 1
    except:
        pass

for i in range(100):
    us = User.objects.create_user(username='user_{}'.format(i), password='pass')
    us.save()
    print('[+] Created user {}'.format(us.username))

for i in range(100):
    q = Question.objects.create(title=fake.sentence(),
                                text=' '.join(fake.sentences()), rating=randint(0, 20),
                                author=list(User.objects.all())[randint(0, len(User.objects.all())-1)])

    taglist = []

    for j in range(3):
        r = randint(0, count - 1)
        # print(r)
        taglist.append(list(Tag.objects.all())[r])

    # print(taglist)
    q.tags.set(taglist)
    q.save()

    print('[+] Created question {}'.format(q.title))
