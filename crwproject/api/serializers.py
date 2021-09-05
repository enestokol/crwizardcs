from xml.dom import minidom

import pandas as pd
from rest_framework import serializers
from ..xml_app.models import File
import xml.etree.ElementTree as et


# Extensions
class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''
        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


# Serializers

class FileSerializer(serializers.ModelSerializer):
    status = ChoiceField(choices=File.STATUS_CHOICES)

    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ['status', 'status_note', 'created_by', 'created_at', 'updated_by', 'updated_at']


class FileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ['status', 'status_note', 'created_by', 'created_at', 'updated_by', 'updated_at']


class FileDiffSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id','name', 'original_path', 'updated_file']


class FileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file', 'original_path']
        read_only_fields = ['file', 'status', 'status_note', 'created_by', 'created_at', 'updated_by', 'updated_at']


class FileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['original_path']
        read_only_fields = ['status', 'status_note', 'created_by', 'created_at', 'updated_by', 'updated_at']
