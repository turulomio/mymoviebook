# Generated by Django 4.2 on 2023-04-22 03:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mymoviebook', '0005_alter_films_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='films',
            old_name='id_dvd',
            new_name='dvd',
        ),
    ]
