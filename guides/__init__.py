from django.conf import settings
import os 

os.makedirs(os.path.join(settings.MEDIA_ROOT, "guides_featured_image"), exist_ok=True)