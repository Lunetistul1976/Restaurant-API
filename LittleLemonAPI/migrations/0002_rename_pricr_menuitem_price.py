# Generated by Django 4.2.3 on 2023-09-17 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menuitem',
            old_name='pricr',
            new_name='price',
        ),
    ]
