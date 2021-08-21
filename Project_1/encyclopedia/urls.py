from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("notfound", views.notFound, name="notfound"),
    path("wiki/<str:page>", views.wikiPage, name="wikipage"),
    path("search", views.searchPage, name="searchpage"),
    path("newpage", views.newPage, name="newpage"),
    path("edit/<str:page>", views.editPage, name="edit")
]
