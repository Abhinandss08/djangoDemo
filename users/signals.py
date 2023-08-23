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


def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()


post_save.connect(createProfile, sender=User)
post_save.connect(profileUpdated, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
