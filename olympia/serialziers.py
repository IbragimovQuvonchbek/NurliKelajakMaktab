from rest_framework.serializers import ModelSerializer
from .models import Olimpiada25082024


class Olimpiada25082024Serializer(ModelSerializer):
    class Meta:
        model = Olimpiada25082024
        fields = '__all__'
