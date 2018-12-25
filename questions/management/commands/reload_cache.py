from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    help = "Reload caches for hot tags and users"
    def handle(self, *args, **options):
        pass