from django.db import models


class Picture(models.Model):
    """
    Модель изображения
    """
    picture = models.ImageField(blank=True)

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

    def __str__(self):
        return str(self.id)
