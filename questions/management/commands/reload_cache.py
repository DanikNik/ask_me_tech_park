from django.core.management.base import BaseCommand
from questions.models import Question
from django.core.cache import cache


class Command(BaseCommand):
    help = "Reload caches for hot tags and users"

    def handle(self, *args, **options):
        cache.clear()
        print("[+] Cleared cache")
        questions = Question.objects.order_by("rating")[:10]
        taglist = [list(question.tags.all()) for question in questions]
        cached_tags = []
        for row in taglist:
            for elem in row:
                cached_tags.append(elem)
        cached_tags = list(set(cached_tags))

        for i in range(len(cached_tags[:7])):
            print("[+] Pushed tag {} in cache as tag_{}".format(cached_tags[i], i))
            cache.set("tag_{}".format(i), cached_tags[i])

        cache.set("cached_tags_num", i+1)
        print("[+] Cached tags num {}".format(i+1))
