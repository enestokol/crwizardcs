from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from crwproject.api.serializers import FileCreateSerializer, FileSerializer
from crwproject.api.tasks import *


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    permission_classes = (AllowAny,)
    default_serializer_class = FileSerializer
    serializer_classes = {
        'create': FileCreateSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_serializer_context(self):
        context = super(self.__class__, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        task = parse_xml_file.delay(serializer.data)
        return Response({'status': 'Started',
                         'task-id': task.id})
