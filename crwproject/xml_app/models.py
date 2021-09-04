from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


def upload_to(instance, filename):
    return f'uploads/{filename}'


def max_file_size(value):
    max_upload_size = "10485760"
    if value.size > int(max_upload_size):
        raise ValidationError('Max file size you can upload is 10 MB.')


class Utility(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(app_label)s_%(class)s_created_by',
                                   blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(app_label)s_%(class)s_updated_by',
                                   blank=True, null=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(auto_now=True)
    note = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class File(Utility):
    ACCEPTED = '1'
    REJECTED = '2'
    PENDING = '3'
    STATUS_CHOICES = [
        (ACCEPTED, 'ACCEPTED'),
        (REJECTED, 'REJECTED'),
        (PENDING, 'PENDING'),
    ]
    name = models.CharField(max_length=255)
    original_path = models.URLField(max_length=255)
    file = models.FileField(upload_to=upload_to,
                            validators=[FileExtensionValidator(
                                allowed_extensions=['xml']),
                                max_file_size])

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=PENDING
    )
    status_note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
