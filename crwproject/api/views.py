import datetime
import os

from django.core import files
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from crwproject.api.serializers import FileCreateSerializer, FileSerializer, FileListSerializer, FileUpdateSerializer, \
    FileDiffSerializer
from crwproject.api.tasks import *


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    permission_classes = (AllowAny,)
    default_serializer_class = FileSerializer
    serializer_classes = {
        'list': FileListSerializer,
        'create': FileCreateSerializer,
        'update': FileUpdateSerializer,
        'retrieve': FileUpdateSerializer,
        'diff_check': FileDiffSerializer
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_serializer_context(self):
        context = super(self.__class__, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    @action(detail=True, methods=['GET'], name='XML Diff Check', url_path='diff-check', url_name='diff_check')
    def diff_check(self, request, pk=None):
        queryset = get_object_or_404(File, pk=pk)
        if queryset.is_active:
            serializer = self.get_serializer(queryset, many=False)
            with requests.get(serializer.data['original_path']) as response:
                if response.headers['content-type'] == 'text/xml':
                    lf = tempfile.NamedTemporaryFile()
                    xml_content = et.tostring(et.fromstring(response.content), xml_declaration=True, encoding='utf-8')
                    lf.write(xml_content)
                    now = datetime.datetime.now()

                    queryset.updated_file.save(
                        os.path.splitext(serializer.data['name'])[0] + "_{0}{1}{2}{3}{4}{5}.xml".format(now.year,
                                                                                                        now.month,
                                                                                                        now.day,
                                                                                                        now.hour,
                                                                                                        now.minute,
                                                                                                        now.second),
                        django.core.files.File(lf))

            # Diff code

            """
            "file" will be compared to "updated_file". then the necessary functions will be run.
             
            """

            # Finally, the file will replace the new updated_file.
            queryset.file.save(
                os.path.splitext(serializer.data['name'])[0] + "_{0}{1}{2}{3}{4}{5}.xml".format(now.year,
                                                                                                now.month,
                                                                                                now.day,
                                                                                                now.hour,
                                                                                                now.minute,
                                                                                                now.second),
                files.File(lf))
            queryset.updated_file.delete()

            return Response({'status': 'Ok'}, status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        opr = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(opr, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        task = parse_xml_file.delay(serializer.data)
        return {'status': 'Started', 'task-id': task.id}
