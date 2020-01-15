from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from questions.models import Question, Answer, Tag
from django.core.cache import cache


class Command(BaseCommand):
    help = "Reload caches for hot tags and users"

    def handle(self, *args, **options):
        cache.clear()
        print("[+] Cleared cache")
        print("[+] Pushing tags in cache...")

        cached_tags = {}
        for tag in Tag.objects.all():
            cached_tags[tag] = 0

        for question in Question.objects.all():
            tags = question.tags.all()
            for tag in tags:
                cached_tags[tag] += 1

        cached_tags_list = [tag[0] for tag in sorted(cached_tags.items(), key=lambda x: x[1])][:20]

        if len(cached_tags_list) == 0:
            cache.set("cached_tags_num", 0)
            print("[+] Cached tags num {}".format(0))
        else:
            count = 0
            for i in range(len(cached_tags_list)):
                print("[+] Pushed tag {} in cache as tag_{}".format(cached_tags_list[i], i))
                cache.set("tag_{}".format(i), cached_tags_list[i])
                count = i

            cache.set("cached_tags_num", count + 1)
            print("[+] Cached tags num {}".format(count + 1))

        print()

        print("[+] Pushing users in cache...")

        cached_users = set()
        i = 0

        from datetime import timedelta
        from django.utils import timezone
        some_day_last_week = timezone.now().date() - timedelta(days=7)
        monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
        questions = Question.objects.filter(date_time__gte=monday_of_last_week).order_by("rating").all()

        for question in questions:
            cached_users.add(question.author)

        cached_users = list(cached_users)

        if len(cached_users) == 0:
            cache.set("cached_users_num", i)
            print("[+] Cached users num {}".format(i))
        else:
            count = 0
            for i in range(len(cached_users[:20])):
                print("[+] Pushed user {} in cache as user_{}".format(cached_users[i], i))
                cache.set("user_{}".format(i), cached_users[i])
                count = i

            cache.set("cached_users_num", count + 1)
            print("[+] Cached users num {}".format(count + 1))
