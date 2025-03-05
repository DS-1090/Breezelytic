
from django.contrib import admin
from django.urls import path
from .views import setLocID, fetchLocData, sendtoApp, fetchrecords
urlpatterns = [
    path('admin/', admin.site.urls),
    path('setLocID/', setLocID),
    path('fetchLocData/', fetchLocData, name="fetchLocData"),
    path('sendtoApp/', sendtoApp),
    path('fetchrecords/', fetchrecords)
]
