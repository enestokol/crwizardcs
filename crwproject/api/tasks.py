from __future__ import absolute_import
import django
import requests
from django.core.files.temp import NamedTemporaryFile
from django.core.mail import send_mail
from crwproject.celery import app
from crwproject.xml_app.models import File


@app.task
def sendEmail(_subject, _message, _to):
    mail_sent = send_mail(_subject, _message, 'noreply@example.com', [_to])
    return mail_sent


@app.task(bind=True)
def parse_xml_file(self, serializer):
    filename = serializer["name"]
    url = serializer["original_path"]

    with requests.get(url) as response:
        print(response.headers['content-type'])
        if response.headers['content-type'] == 'text/xml':

            filetemp = NamedTemporaryFile()
            filetemp.write(response.content)
            filetemp.flush()

            File.objects.create(
                name=filename,
                original_path=url,
                file=(filename, django.core.files.File(filetemp)),
                status=1
            )
        else:
            File.objects.create(
                name=filename,
                original_path=url,
                status=2
            )
