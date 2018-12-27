from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from questions.models import Question, Answer
from django.core.cache import cache


class UserCounter:
    def __init__(self, user, count):
        self.user = user
        self.count = count

    def key(self):
        return self.count


class MaxStack:
    def __init__(self, data_size):
        self.data = list()
        self.size = data_size

    def push(self, elem):
        self.data.append(elem)
        self.data = sorted(self.data, key=lambda user_c: user_c[1], reverse=True)[:self.size]

    def get_data(self):
        return [elem[0] for elem in self.data]


class Command(BaseCommand):
    help = "Reload caches for hot tags and users"

    def handle(self, *args, **options):
        cache.clear()
        print("[+] Cleared cache")
        print("[+] Pushing tags in cache...")
        questions = Question.objects.order_by("rating")[:10]
        taglist = [list(question.tags.all()) for question in questions]
        cached_tags = []
        for row in taglist:
            for elem in row:
                cached_tags.append(elem)
        cached_tags = list(set(cached_tags))

        for i in range(len(cached_tags[:10])):
            print("[+] Pushed tag {} in cache as tag_{}".format(cached_tags[i], i))
            cache.set("tag_{}".format(i), cached_tags[i])

        cache.set("cached_tags_num", i + 1)
        print("[+] Cached tags num {}".format(i + 1))

        print()

        print("[+] Pushing users in cache...")
        users = User.objects.all()
        user_answer_count = MaxStack(10)
        for user in users:
            user_answers = Answer.objects.filter(author=user).count()
            user_answer_count.push([user, user_answers])

        cached_users = user_answer_count.get_data()
        for i in range(len(cached_users)):
            print("[+] Pushed user {} in cache as user_{}".format(cached_users[i], i))
            cache.set("user_{}".format(i), cached_users[i])

        cache.set("cached_users_num", i + 1)
        print("[+] Cached users num {}".format(i + 1))
