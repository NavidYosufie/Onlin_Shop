from django.db.models.signals import post_save
from .models import User
from django.dispatch import receiver
from .models import Profile
from django.db.models.signals import pre_save
import os
from django.conf import settings
from django.core.files.storage import default_storage

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(pre_save, sender=Profile)
def delete_previous_profile_picture(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_user = Profile.objects.get(pk=instance.pk)
        except User.DoesNotExist:
            return
        if old_user.image != instance.image:
            if os.path.isfile(os.path.join(settings.MEDIA_ROOT, old_user.image.name)):
                default_storage.delete(old_user.image.name)