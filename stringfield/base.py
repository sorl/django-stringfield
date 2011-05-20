from django.db import models
from django.utils.translation import ugettext_lazy as _


class StringField(models.CharField):
    description = _("String")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 255)
        super(models.CharField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "TextField"

    def to_python(self, value):
        if isinstance(value, basestring) or value is None:
            return value
        return smart_unicode(value)

    def get_prep_value(self, value):
        return self.to_python(value)

    def formfield(self, **kwargs):
        defaults = {'max_length': self.max_length}
        defaults.update(kwargs)
        return super(CharField, self).formfield(**defaults)

    def db_type(self, connection):
        if connection.vendor == 'postgresql':
            return 'character varying'
        if connection.vendor == 'mysql':
            return 'VARCHAR (65528)'
        return 'TEXT'

    def south_field_triple(self):
        from south.modelsinspector import introspector
        name = '%s.%s' % (self.__class__.__module__ , self.__class__.__name__)
        args, kwargs = introspector(self)
        return name, args, kwargs

