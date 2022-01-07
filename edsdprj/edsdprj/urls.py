from django.contrib import admin
from django.urls import path
from mainapp.views import MainView, GuessView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', MainView.as_view(),  name='index'),
    path('guesses', GuessView.as_view(), name='guesses')
]
