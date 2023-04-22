# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Covers(models.Model):
    films_id = models.IntegerField(blank=True, null=True)
    cover = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'covers'


class Films(models.Model):
    id_films = models.AutoField(primary_key=True)
    savedate = models.DateField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    id_dvd = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'films'


class Globals(models.Model):
    id = models.IntegerField(primary_key=True)
    global_field = models.TextField(db_column='global', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'globals'
