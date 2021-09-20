import datetime
import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.public.picture.helpers import check_width_height, check_open_image, check_degree, create_picture_in_db
from api.public.picture.serializers import PictureSerializer
from picture.models import Picture


class PictureViewSet(viewsets.ModelViewSet):
    """
    Предтавление для получения списка картинок и создания картинки
    """

    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

    def create(self, request, *args, **kwargs):
        images = dict((request.data).lists())['file']
        flag = 1
        arr = []
        for img_name in images:
            print(img_name)
            file_serializer = self.get_serializer(data={'picture': img_name})
            if file_serializer.is_valid(raise_exception=True):
                file_serializer.save()
                arr.append(file_serializer.data)
            else:
                flag = 0

        if flag == 1:
            return Response(arr, status=status.HTTP_201_CREATED)
        else:
            return Response(arr, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def resize(self, request, pk=None):
        obj_picture = self.get_object()
        width = self.request.query_params.get('width')
        height = self.request.query_params.get('height')

        # Проверяем существование изображения
        parent_picture = check_open_image(obj_picture.picture)
        # Проверяем параметры
        width, height = check_width_height(parent_picture, width, height)

        name_children_picture = f'new_file_with_width_{width}_height_{height}_{obj_picture.picture}'
        children_picture_resize = parent_picture.resize((width, height), Image.ANTIALIAS)
        children_picture_resize.save(name_children_picture)

        # Сохраняем новое изображение в БД
        children_picture = create_picture_in_db(name_children_picture)
        serializer = self.get_serializer(children_picture)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def rotate(self, request, pk=None):
        obj_picture = self.get_object()
        degree = self.request.query_params.get('degree')

        # Проверяем существование изображения
        parent_picture = check_open_image(obj_picture.picture)
        # Проверяем параметры
        degree = check_degree(degree)
        if not degree:
            serializer = self.get_serializer(obj_picture)
            return Response(serializer.data)
        else:
            name_children_picture = f'new_file_with_degree_{degree}_{obj_picture.picture}'
            children_picture_rotate = parent_picture.rotate(degree)
            children_picture_rotate.save(name_children_picture)

            # Сохраняем новое изображение в БД
            children_picture = create_picture_in_db(name_children_picture)
            serializer = self.get_serializer(children_picture)
            return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def convert(self, request, pk=None):
        obj_picture = self.get_object()
        # Проверяем существование изображения
        parent_picture = check_open_image(obj_picture.picture)
        name_file = str(obj_picture.picture).split('.')[0]
        if parent_picture.format == 'JPEG':
            name_children_picture = f'new_file_convert_{name_file}.png'
            children_picture_convert = parent_picture.save(name_children_picture, 'png')
        else:
            name_children_picture = f'new_file_convert_{name_file}.jpeg'
            children_picture_convert = parent_picture.save(name_children_picture, 'jpeg')
        # Сохраняем новое изображение в БД
        children_picture = create_picture_in_db(name_children_picture)
        serializer = self.get_serializer(children_picture)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def all(self, request, pk=None):
        obj_picture = self.get_object()
        width = self.request.query_params.get('width')
        height = self.request.query_params.get('height')
        degree = self.request.query_params.get('degree')

        # Проверяем существование изображения
        parent_picture = check_open_image(obj_picture.picture)
        # Проверяем параметры
        width, height = check_width_height(parent_picture, width, height)
        degree = check_degree(degree)

        name_children_picture = f'new_file_with_width_{width}_height_{height}_degree_{degree}_{obj_picture.picture}'
        children_picture_resize = parent_picture.resize((width, height), Image.ANTIALIAS)
        children_picture_resize = children_picture_resize.rotate(degree)
        children_picture_resize.save(name_children_picture)

        # Сохраняем новое изображение в БД
        children_picture = create_picture_in_db(name_children_picture)
        serializer = self.get_serializer(children_picture)
        return Response(serializer.data)
