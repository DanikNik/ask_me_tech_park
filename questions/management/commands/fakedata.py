from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker

# from account.models import Person
from questions.models import Question, Tag

fake = Faker()


class Command(BaseCommand):
    help = 'Generates fake data'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int)
        parser.add_argument('--questions', type=int)
        parser.add_argument('--tags', type=int)

    def handle(self, *args, **options):
        if options['users'] is not None:
            for _ in range(options['users']):
                _user = User.objects.create(username=fake.user_name(), email=fake.email())
                _user.save()
                print('[+] Created user {}'.format(_user.username))

        if options['questions'] is not None:
            for _ in range(options['questions']):
                q = Question.objects.create(title=fake.sentence(),
                                            text=fake.sentences())
                q.save()
                print('[+] Created question {}'.format(q.title))

        if options['tags'] is not None:
            for _ in range(options['tags']):
                tag = Tag.objects.create(text=fake.word())
                tag.save()
                print('[+] Created tag {}'.format(tag.text))
