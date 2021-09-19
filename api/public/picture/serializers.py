from PIL import Image
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from picture.models import Picture, PictureInfo


class PictureListCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра списка картинок и добавления картинки
    """

    class Meta:
        model = Picture
        fields = '__all__'


class PictureRetrieveDestroySerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра конкретной картинки и удаления
    """

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(source='picture_information.name', read_only=True)
    width = serializers.IntegerField(source='picture_information.width', read_only=True)
    height = serializers.IntegerField(source='picture_information.height', read_only=True)
    parent_picture = serializers.IntegerField(source='picture_information.parent_picture.id',
                                              read_only=True, allow_null=True)

    class Meta:
        model = Picture
        fields = ('id', 'name', 'url', 'picture', 'width', 'height', 'parent_picture')


class PictureResizeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изменения размеров конкретной картинки
    """

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(source='picture_information.name', read_only=True)
    width = serializers.IntegerField(label='Ширина', source='picture_information.width',
                                     validators=[MinValueValidator(1), MaxValueValidator(10000)])
    height = serializers.IntegerField(label='Высота', source='picture_information.height',
                                      validators=[MinValueValidator(1), MaxValueValidator(10000)])
    parent_picture = serializers.IntegerField(source='picture_information.parent_picture.id', read_only=True,
                                              allow_null=True)

    class Meta:
        model = Picture
        fields = '__all__'
        read_only_fields = ('id', 'name', 'url', 'picture', 'parent_picture')

    def create(self, validated_data):
        return self.initial_data.get('children_picture')
