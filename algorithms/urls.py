
from django.urls import path
from .views import fibonacci,ackermann,factorial,health_check

urlpatterns = [
    path('fibonacci/',fibonacci),
    path('ackermann/',ackermann),
    path('factorial/',factorial),
    path('ping/',health_check)
]
