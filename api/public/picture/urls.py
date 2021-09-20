from django.urls import path
from rest_framework import routers

from api.public.picture.views import PictureViewSet

app_name = 'picture'


router = routers.SimpleRouter()
router.register('', PictureViewSet, basename='images')

urlpatterns = [
]

urlpatterns += router.urls
