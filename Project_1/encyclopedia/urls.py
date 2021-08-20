from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page>", views.wikiPage, name="wikipage"),
    path("search", views.searchPage, name="searchpage")
]
