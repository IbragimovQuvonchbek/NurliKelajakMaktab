from rest_framework.serializers import ModelSerializer
from .models import StudentResult, Student


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class StudentResultSerializer(ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = StudentResult
        fields = '__all__'
