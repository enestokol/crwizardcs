import os

from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from crwproject.api.tasks import *


@receiver(pre_save, sender=File)
def send_email_on_create_from_file(sender, instance, **kwargs):
    print("8")
    if instance.status == '2':
        print("10")
        _subject = 'About {0}'.format(instance.name)
        _message = '{0} was {1} Due to {2}'.format(
            instance.name,
            instance.status,
            instance.status_note)
        # _to = instance.created_by.email
        # sendEmail.delay(_subject, _message, _to)


@receiver(post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(pre_save, sender=File)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = File.objects.get(pk=instance.pk).file
    except File.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        try:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
        except Exception:
            return False
