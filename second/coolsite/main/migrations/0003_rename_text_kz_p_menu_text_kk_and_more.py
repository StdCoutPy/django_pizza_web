# Generated by Django 4.2.4 on 2023-08-10 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_p_menu_text_en_p_menu_text_kz_p_menu_text_ru_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='p_menu',
            old_name='text_kz',
            new_name='text_kk',
        ),
        migrations.RenameField(
            model_name='p_menu',
            old_name='title_kz',
            new_name='title_kk',
        ),
    ]
