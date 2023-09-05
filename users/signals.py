from .models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=Profile)
def profileUpdated(sender, instance, created, **kwargs):
    print('Profile Saved!')
    print('Instance:', instance)
    print('Created:', created)


def createProfile(sender, instance, created, **kwargs):
    print('Profile signal triggered..')
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )

# To edit the user data
def updateUser(sender, instance, created, **kwargs):
    profile = instance
    # With one-to-one relationship user can be obtained from profile
    user = profile.user
    # To avoid recursion error or caught up in an infinite profile
    # creation error
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()


post_save.connect(createProfile, sender=User)
post_save.connect(profileUpdated, sender=Profile)
# To update the user whenever the profile is updated this
# will automatically trigger updateUser fn
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
