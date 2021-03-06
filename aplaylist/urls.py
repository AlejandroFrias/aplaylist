"""spotify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("aplaylist", views.index, name="index"),
    path("aplaylist/play-album/<spotify_id>/<device_id>", views.play_album, name="play-album"),
    path(
        "aplaylist/play-album-playlist/<name>/<device_id>",
        views.play_album_playlist,
        name="play-album-playlist",
    ),
]
