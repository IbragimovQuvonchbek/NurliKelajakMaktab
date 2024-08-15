from django.urls import path
from .views import GetAllOlimpiada25082024, GetByTgIdOlimpiada25082024, AddOlimpiada25082024

urlpatterns = [
    path('get-all25082024/', GetAllOlimpiada25082024.as_view(), name='get-all25082024'),
    path('get-bytg25082024/', GetByTgIdOlimpiada25082024.as_view(), name='get-bytg25082024'),
    path('add25082024/', AddOlimpiada25082024.as_view(), name='add-25082024')
]
