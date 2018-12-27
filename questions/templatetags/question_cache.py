from django import template
from django.template.defaultfilters import stringfilter
from django.core.cache import cache

register = template.Library()


@register.simple_tag()
def get_best_tags():
    cached_tags = []
    for i in range(cache.get("cached_tags_num")):
        cached_tags.append(cache.get("tag_{}".format(i)))
    print(cached_tags)
    return cached_tags


@register.simple_tag()
def get_best_users():
    cached_users = []
    for i in range(cache.get("cached_users_num")):
        cached_users.append(cache.get("user_{}".format(i)))
    print(cached_users)
    return cached_users
