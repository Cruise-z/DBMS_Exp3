# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class BookComments(models.Model):
    ISBN = models.OneToOneField('Summary', models.DO_NOTHING, db_column='ISBN', primary_key=True)  # Field name made lowercase.
    User_id = models.ForeignKey('Users', models.DO_NOTHING, db_column='User_id')  # Field name made lowercase.
    Time = models.DateTimeField(db_column='Time', auto_now=True)  # Field name made lowercase.
    Remark = models.CharField(db_column='Remark', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'book_comments'
        unique_together = (('ISBN', 'User_id', 'Time'),)


class BookScores(models.Model):
    ISBN = models.OneToOneField('Summary', models.DO_NOTHING, db_column='ISBN', primary_key=True)  # Field name made lowercase.
    User_id = models.ForeignKey('Users', models.DO_NOTHING, db_column='User_id')  # Field name made lowercase.
    Score = models.FloatField(db_column='Score', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'book_scores'
        unique_together = (('ISBN', 'User_id'),)


class Summary(models.Model):
    ISBN = models.CharField(db_column='ISBN', primary_key=True, max_length=13)  # Field name made lowercase.
    Title = models.CharField(db_column='Title', max_length=255, blank=True, null=True)  # Field name made lowercase.
    Author = models.CharField(db_column='Author', max_length=255, blank=True, null=True)  # Field name made lowercase.
    Price = models.FloatField(db_column='Price', blank=True, null=True)  # Field name made lowercase.
    Press = models.CharField(db_column='Press', max_length=255, blank=True, null=True)  # Field name made lowercase.
    Score = models.FloatField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    Num_of_scorers = models.PositiveIntegerField(db_column='Num_of_scorers', blank=True, null=True)  # Field name made lowercase.
    Num_of_comments = models.PositiveIntegerField(db_column='Num_of_comments', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'summary'


class Users(models.Model):
    Id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    Password = models.CharField(db_column='Password', max_length=255, blank=True, null=True)  # Field name made lowercase.
    Name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    Sex = models.IntegerField(db_column='Sex', blank=True, null=True)  # Field name made lowercase.
    Telephone = models.CharField(db_column='Telephone', max_length=255, blank=True, null=True)  # Field name made lowercase.
    City = models.CharField(db_column='City', max_length=255, blank=True, null=True)  # Field name made lowercase.
    Email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)  # Field name made lowercase.
    Authtype = models.IntegerField(db_column='Authtype', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'users'
