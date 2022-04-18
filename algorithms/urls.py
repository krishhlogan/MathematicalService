from django.urls import path
from .views import fibonacci, ackermann, factorial, health_check, flush_cache

urlpatterns = [
    path('fibonacci/', fibonacci),
    path('ackermann/', ackermann),
    path('factorial/', factorial),
    path('ping/', health_check),
    path('flushAll/', flush_cache)
]
