
from django.urls import path
from .views import fibonacci,ackermann,factorial

urlpatterns = [
    path('fibonacci/',fibonacci),
    path('ackermann/',ackermann),
    path('factorial/',factorial)
]
