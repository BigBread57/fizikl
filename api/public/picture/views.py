import os
from io import BytesIO

import requests

from PIL import Image
from django.core.files.base import ContentFile
from rest_framework import generics, status, exceptions
from rest_framework.response import Response

from api.public.picture.serializers import PictureRetrieveDestroySerializer, PictureResizeSerializer, \
    PictureListCreateSerializer
from picture.models import Picture, PictureInfo


class PictureListCreateApiView(generics.ListCreateAPIView):
    """
    Предтавление для получения списка картинок и создания картинки
    """

    queryset = Picture.objects.all()
    serializer_class = PictureListCreateSerializer


class PictureRetrieveDestroyApiView(generics.RetrieveDestroyAPIView):
    """
    Предтавление для получения конкретной картинки и ее удаления
    """

    queryset = Picture.objects.all()
    serializer_class = PictureRetrieveDestroySerializer
    lookup_fields = ['id']


class PictureResizeApiView(generics.CreateAPIView):
    """
    Предтавление для изменения размера картинки
    """

    queryset = Picture.objects.all()
    serializer_class = PictureResizeSerializer

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs.get('pk'))

    def create(self, request, *args, **kwargs):
        new_name_picture = ''
        obj_picture = PictureInfo.objects.get(picture_id=self.kwargs.get('pk'))
        width = request.data.get('width')
        height = request.data.get('height')

        if width == '' and height == '':
            raise exceptions.ValidationError(detail={
                'message': 'Необходимо ввести не менее одного значения'})

        if width:
            new_name_picture = f'{new_name_picture}_{width}'
        else:
            width = obj_picture.width
            new_name_picture = f'{new_name_picture}_0'

        if height:
            new_name_picture = f'{new_name_picture}_{height}'
        else:
            height = obj_picture.height
            new_name_picture = f'{new_name_picture}_0'

        try:
            parent_picture = Image.open(obj_picture.picture.picture)
        except IOError:
            return Response(status=status.HTTP_204_NO_CONTENT, data={
                'message': 'Невозможно найти изображение'})

        data_for_serializer = {'csrfmiddlewaretoken': request.data.get('csrfmiddlewaretoken'),
                               'width': width, 'height': height}
        serializer = self.get_serializer(data=data_for_serializer)
        serializer.is_valid(raise_exception=True)

        # Формируем новое название измененного файла
        format_children_picture = obj_picture.name.split('.')[-1:][0]
        name_children_picture = f'{obj_picture.name}{new_name_picture}.{format_children_picture}'

        children_picture_resize = parent_picture.resize((int(width), int(height)), Image.ANTIALIAS)
        children_picture_resize.save(name_children_picture)

        img = Image.open(name_children_picture)

        if format_children_picture in ('jpg', 'jpeg'):
            format_children_picture = 'jpeg'
        else:
            format_children_picture = 'png'

        print(format_children_picture)
        with BytesIO() as buf:
            img.save(buf, format_children_picture)
            picture_bytes = buf.getvalue()
        django_file = ContentFile(picture_bytes)

        children_picture = Picture(url=obj_picture.picture.url)
        children_picture.picture.save(name_children_picture, django_file)
        children_picture.save()
        os.remove(name_children_picture)

        PictureInfo.objects.create(name=name_children_picture, picture=children_picture,
                                   width=width, height=height, parent_picture=obj_picture.picture)
        serializer = self.get_serializer(data={'csrfmiddlewaretoken': request.data.get('csrfmiddlewaretoken'),
                                               'width': width, 'height': height,
                                               'children_picture': children_picture})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
