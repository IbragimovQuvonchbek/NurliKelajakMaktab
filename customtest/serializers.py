from rest_framework.serializers import ModelSerializer
from .models import Results, Tests, TestFile


class ResultSerializer(ModelSerializer):
    class Meta:
        model = Results
        fields = '__all__'


class TestSerializer(ModelSerializer):
    class Meta:
        model = Tests
        fields = '__all__'


class TestFileSerializer(ModelSerializer):
    class Meta:
        model = TestFile
        fields = ['file_id', ]
