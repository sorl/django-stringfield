from django import forms
from django.core import validators
from django.db import models
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _


class StringField(models.Field):
    description = _("String")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 500)
        super(StringField, self).__init__(*args, **kwargs)

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
        return super(StringField, self).formfield(**defaults)

    def db_type(self, connection=None):
        if connection is None:
            # Django < 1.2 doesn't have connection
            from django.conf import settings
            name = settings.DATABASE_ENGINE.split('.')[-1].split('_')[0]
            if name == 'postgis':
                vendor = 'postgresql'
            else:
                vendor = name
        else:
            vendor = connection.vendor
        if vendor == 'postgresql':
            return 'character varying'
        if vendor == 'mysql':
            return 'VARCHAR (65528)'
        if vendor == 'oracle':
            return 'VARCHAR2 (4000)'
        return 'TEXT'

    def south_field_triple(self):
        from south.modelsinspector import introspector
        name = '%s.%s' % (self.__class__.__module__ , self.__class__.__name__)
        args, kwargs = introspector(self)
        kwargs.pop('max_length', None)
        return name, args, kwargs


class EmailField(StringField):
    description = _("E-mail address")
    default_validators = [validators.validate_email]

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.EmailField}
        defaults.update(kwargs)
        return super(EmailField, self).formfield(**defaults)


class URLField(StringField):
    description = _("URL")

    def __init__(self, *args, **kwargs):
        verify_exists = kwargs.pop('verify_exists', False)
        super(URLField, self).__init__(*args, **kwargs)
        self.validators.append(validators.URLValidator(verify_exists=verify_exists))

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.URLField}
        defaults.update(kwargs)
        return super(URLField, self).formfield(**defaults)


class SlugField(StringField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('db_index', True)
        super(SlugField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.SlugField}
        defaults.update(kwargs)
        return super(SlugField, self).formfield(**defaults)

