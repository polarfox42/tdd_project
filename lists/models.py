from django.db import models


class List(models.Model):
    '''To-Do list'''
    pass


class Item(models.Model):
    '''List item'''
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.PROTECT)
