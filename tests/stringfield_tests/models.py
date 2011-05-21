from django.db import models
from stringfield import StringField


class Item(models.Model):
    name = StringField(max_length=1)

