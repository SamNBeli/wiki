from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("wiki", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("random", views.random_entry, name="random"),
    path("new", views.new_entry, name = "new"),
    path("edit/<str:title>", views.edit_entry, name = "edit")
]
