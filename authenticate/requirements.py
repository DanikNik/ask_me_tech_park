from django.contrib.auth.decorators import user_passes_test

def person_assigned(user):
    print(user.person)
    try:
        assert (user.person.user == user)

    except:
        return False