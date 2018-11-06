#! /usr/bin/env python3

import sys
import os
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ask_me_tech_park.settings'
django.setup()

print('[+] Set up environment')

# from account.models import Person
from questions.models import Question, Tag
from django.contrib.auth.models import User

alphabet = ['alpha', 'beta', 'gamma', 'delta', 'kappa']
admin = User.objects.create_superuser(username='admin', password='admin', email='root@admin.com')
admin.save()
# Person.objects.create(name='ADMIN', surname='ADMIN', nickname='ADMIN', user=admin)
print('[+] Created superuser')
for i in range(5):
    # us = User.objects.create_user(username='user{}'.format(alphabet[i]), password='pass')
    # us.save()
    # print('[+] Created user {}'.format(us.username))
    # person = Person.objects.create(name='Person', surname=alphabet[i].capitalize(), nickname="Person_{}".format(alphabet[i]),
    #                       user=us)
    # person.save()
    # print('[+] Created person {}'.format(person.nickname))

    tag = Tag.objects.create(text=alphabet[i])
    tag.save()
    print('[+] Created tag {}'.format(tag.text))
    q = Question.objects.create(title="Question {}".format(alphabet[i]),
                                text="Question #{} descr".format(alphabet[i]))
    q.save()
    print('[+] Created question {}'.format(q.title))
