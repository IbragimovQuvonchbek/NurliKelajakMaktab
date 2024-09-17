from django.urls import path
from .views import GetStudentById

urlpatterns = [
    path('results/', GetStudentById.as_view(), name="get-result-by-id")
]