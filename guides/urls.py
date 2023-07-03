from django.urls import path
from .views import *

app_name = "guides"

urlpatterns = [
    path('articles/', HomePageView.as_view(), name="home_url"),
    path('articles/<slug:category_slug>/', HomePageView.as_view(), name="category_url"),
    path('<slug:url_slug>/', BlogView.as_view(), name="blog_url"),
]