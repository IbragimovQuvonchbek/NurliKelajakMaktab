from django.urls import path
from .views import GetAllTestsAPI, GetTestByIdAPI, CheckUserSolvedAPI, CheckTestByIdAPI

urlpatterns = [
    path('all-tests/', GetAllTestsAPI.as_view(), name='get-all-test'),
    path('all-tests/<int:pk>/', GetTestByIdAPI.as_view(), name='get-test-by-id'),
    path('user-solved/<int:pk>/', CheckUserSolvedAPI.as_view(), name='user-solved'),
    path('check-test/<int:pk>/', CheckTestByIdAPI.as_view(), name='check-test'),

]
