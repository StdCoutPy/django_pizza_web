from modeltranslation.translator import register, TranslationOptions
from main.models import  P_Menu



@register(P_Menu)
class P_MenuTranslationOptions(TranslationOptions):
    fields = ('title' , 'text')