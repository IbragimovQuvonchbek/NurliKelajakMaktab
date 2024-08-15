from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .models import Olimpiada25082024
from .serialziers import Olimpiada25082024Serializer
from rest_framework.response import Response


class GetAllOlimpiada25082024(APIView):
    def get(self, request):
        users = Olimpiada25082024.objects.all()
        serializer = Olimpiada25082024Serializer(users, many=True)
        return Response(serializer.data)


class AddOlimpiada25082024(APIView):
    def post(self, request):
        serializer = Olimpiada25082024Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetByTgIdOlimpiada25082024(APIView):
    def get(self, request):
        telegram_id = request.query_params.get('telegram_id')
        if telegram_id:
            users = Olimpiada25082024.objects.filter(telegram_id=telegram_id)
            serializer = Olimpiada25082024Serializer(users, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
