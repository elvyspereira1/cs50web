from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/search/', views.search, name='search'),
    path('wiki/new_page/', views.new_page, name='new_page'),
    path("wiki/random/", views.random_page, name="random_page"),
    path("wiki/get_entries/", views.get_entries, name="get_entries"),
    path("wiki/<str:title>/edit/", views.edit_page, name="edit_page"),
    path('wiki/<str:title>/', views.wiki_entry, name='wiki_entry')
]
