from django.db.models.signals import pre_save
from django.dispatch import receiver
from crwproject.api.tasks import *


@receiver(pre_save, sender=File)
def send_email_on_create_from_file(sender, instance, **kwargs):
    if instance.status == '2':
        _subject = 'About {0}'.format(instance.name)
        _message = '{0} was {1} Due to {2}'.format(
            instance.name,
            instance.status,
            instance.status_note)
        # _to = instance.created_by.email
        # sendEmail.delay(_subject, _message, _to)
