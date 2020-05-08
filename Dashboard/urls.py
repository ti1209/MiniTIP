from . import views
from django.urls import path

urlpatterns = [
    path('threat/', views.threat, name='threat'),
    path('device/', views.device, name='device'),
    path('globalist/', views.globalist, name='globalist')
]