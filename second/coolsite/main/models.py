from django.utils.translation import gettext_lazy as _


from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class P_Menu(models.Model):
    title = models.CharField('Название', max_length=50)
    text = models.TextField('Описание')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    count = models.IntegerField('Колличество', default=1, validators=[MaxValueValidator(100), MinValueValidator(1)])
    in_basket = models.BooleanField(default=False)
    which_product = models.TextField(default='pizza')
    price = models.IntegerField('Цена', default=0, validators=[MaxValueValidator(10000000), MinValueValidator(0)])

    def __str__(self):
        return self.title



