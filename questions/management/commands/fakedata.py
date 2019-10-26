from random import randint

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker

# from account.models import Person
from questions.models import Question, Tag, Answer

fake = Faker()


class Command(BaseCommand):
    help = 'Generates fake data'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int)
        parser.add_argument('--questions', type=int)
        parser.add_argument('--tags', type=int)
        parser.add_argument('--answers', type=int)

    def handle(self, *args, **options):
        if options['users'] is not None:
            for _ in range(options['users']):
                _user = User.objects.create(username=fake.user_name(),
                                            email=fake.email(),
                                            first_name=fake.first_name(),
                                            last_name=fake.last_name())
                _user.save()
                print('[+] Created user {}'.format(_user.username))

        if options['tags'] is not None:
            for _ in range(options['tags']):
                tag = Tag.objects.create(text=fake.word())
                tag.save()
                print('[+] Created tag {}'.format(tag.text))

        if options['questions'] is not None:
            for _ in range(options['questions']):
                q = Question.objects.create(title=fake.sentence(),
                                            text=' '.join(fake.sentences()), rating=0)

                taglist = []

                for j in range(3):
                    r = randint(0, Tag.objects.count() - 1)
                    # print(r)
                    taglist.append(list(Tag.objects.all())[r])

                # print(taglist)
                q.tags.set(taglist)
                q.save()
                print('[+] Created question {}'.format(q.title))

        if options['answers'] is not None:
            for question in Question.objects.all():
                for _ in range(options['answers']):
                    rnd_user = randint(0, User.objects.count()-1)
                    answer = Answer.objects.create(author=list(User.objects.all())[rnd_user], text=fake.sentence())
                    answer.save()
                    question.answer_set.add(answer)
                    print('[+] Created answer {}'.format(_))
