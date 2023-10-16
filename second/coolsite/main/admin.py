from django import forms
from django.contrib import admin
from .models import *

from modeltranslation.admin import TranslationAdmin
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# Register your models here.
admin.site.register(P_Menu)




class P_MenuAdmin(TranslationAdmin):
    description_ru = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    description_en = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    description_kk = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = P_Menu
        fields = '__all__'
