from django.core.validators import validate_image_file_extension, MinValueValidator, MaxValueValidator
from rest_framework import serializers

from picture.models import Picture


class PictureSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра списка картинок и добавления картинки
    """
    picture = serializers.FileField(validators=[validate_image_file_extension])

    class Meta:
        model = Picture
        fields = '__all__'
