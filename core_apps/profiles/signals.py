import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from config.settings.base import AUTH_USER_MODEL

from .models import Profile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # create a new profile when user is created.
        Profile.objects.create(user=instance)
        logger.info(f"{instance}'s profile has been created.")
    else:
        try:
            # update the profile for the user already created
            profile = Profile.objects.get(user=instance)
            profile.save()
            logger.info(f"{instance}'s profile has been updated.")
        except Profile.DoesNotExist:
            # create a profile for user that already created but don't have a profile
            Profile.objects.create(user=instance)
            logger.info(f"{instance}'s profile has been created.")
