from django.conf import settings
import os 

os.makedirs(os.path.join(settings.MEDIA_ROOT, "doctor_images"), exist_ok=True)
os.makedirs(os.path.join(settings.MEDIA_ROOT, "featured_images"), exist_ok=True)
os.makedirs(os.path.join(settings.MEDIA_ROOT, "images"), exist_ok=True)
os.makedirs(os.path.join(settings.MEDIA_ROOT, "logo"), exist_ok=True)
os.makedirs(os.path.join(settings.MEDIA_ROOT, "homepage"), exist_ok=True)