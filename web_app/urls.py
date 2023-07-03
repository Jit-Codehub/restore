from django.urls import path
from .views import *

app_name = "web_app"

urlpatterns = [
    path("", HomePageView.as_view(), name="home_url"),
    path("doctors/<slug:doctor_slug>/", DoctorPageView.as_view(), name="doctor_url"),
    path('contact-us/', contact, name="contact_us_url"),
    path('services/<slug:service_name>/',services,name='services'),
    path('about-us/',about_us.as_view(),name='about_us'),
]
