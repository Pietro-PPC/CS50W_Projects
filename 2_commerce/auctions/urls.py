from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("listing/<str:id>", views.listing_page, name="listing"),
    path("toggle_watchlist/<str:listing_id>", views.toggle_watchlist, name="toggle_watchlist"),
    path("close_listing/<str:listing_id>", views.close_listing, name="close"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:cat>", views.category, name="category")
]
