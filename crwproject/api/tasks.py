from __future__ import absolute_import
import xml.etree.ElementTree as et
import tempfile

import django
import requests
from bs4 import BeautifulSoup
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
    url = serializer["original_path"]
    file_name = url.split('/')[-1]
    file = File(name=file_name, original_path=url)
    with requests.get(url) as response:
        if response.headers['content-type'] == 'text/xml':
            lf = tempfile.NamedTemporaryFile()
            xml_content = et.tostring(et.fromstring(response.content), xml_declaration=True, encoding='utf-8')
            lf.write(xml_content)

            file.file.save(file_name, django.core.files.File(lf), save=False)
            file.status = 1
            file.save()

            """
            File.objects.create(
                name=file_name,
                original_path=url,
                file=(file_name, django.core.files.File(lf)),
                status=1
            )
            """
        else:
            file.status = 2
            file.save()
            """
            File.objects.create(
                name=file_name,
                original_path=url,
                status=2
            )
            """
