from django.contrib import admin
from django.urls import path, include
from WebScraper.views import *

app_name = "Scraper"

urlpatterns = [
    path('', HomePage, name="HomePage"),
    path('Results', Results, name="SearchResults"),
    path('Archive', Archive, name="Archive"),
    path('Download', Csv, name="CSV"),
]