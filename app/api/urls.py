from django.urls import path
from .views import getRoutes


urlpatterns = [
    path('', view=getRoutes)
]