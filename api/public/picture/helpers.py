import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.response import Response

from picture.models import Picture


def check_open_image(name_image):
    try:
        parent_picture = Image.open(name_image)
    except IOError:
        return Response(status=status.HTTP_204_NO_CONTENT, data={
            'message': 'Невозможно найти изображение'})
    return parent_picture


def check_width_height(parent_picture, width, height):
    """
    Функция для проверки параметров ширины и высоты
    """

    if not width:
        width = parent_picture.width

    if not height:
        height = parent_picture.height

    try:
        int(width)
    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
            'message': 'Ширина должно быть числом от 1 до 10000'})

    try:
        int(height)
    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
            'message': 'Высота должно быть числом от 1 до 10000'})

    if not 0 < int(width) < 10000:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
            'message': 'Ширина должно быть числом от 1 до 10000'})

    if not 0 < int(height) < 10000:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
            'message': 'Высота должно быть числом от 1 до 10000'})

    return int(width), int(height)


def check_degree(degree):
    """
    Функция для проверки параметра градусы
    """
    if not degree:
        return False
    try:
        int(degree)
    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
            'message': 'Поворот изображения выражаются в градусах, которые должны быть числом от 0 до 359'})

    if not 0 < int(degree) < 360:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
            'message': 'Градусы должны быть числом от 0 до 359'})
    return int(degree)


def create_picture_in_db(name_children_picture):
    """
    Функция для создания новой картинки в БД
    """
    img = Image.open(name_children_picture)
    extencion = img.format
    with BytesIO() as buf:
        img.save(buf, extencion)
        picture_bytes = buf.getvalue()
    django_file = ContentFile(picture_bytes)

    children_picture = Picture()
    children_picture.picture.save(name_children_picture, django_file)
    children_picture.save()
    os.remove(name_children_picture)
    return children_picture

