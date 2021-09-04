from rest_framework import serializers
from ..xml_app.models import File


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


class FileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['name', 'original_path']
        read_only_fields = ['status', 'status_note', 'created_by', 'created_at', 'updated_by', 'updated_at']
