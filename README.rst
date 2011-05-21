
django-stringfield
==================

A field intended for strings that typically has a length less than 500
characters.  django-stringfield tries to not to enforce length on database level
if possible but different databases have different limitations. Currently
implemented as:

PostgreSQL
    ``character varying``

MySQL
    ``VARCHAR (65528)`` [#f1]_

Oracle
    ``VARCHAR2 (4000)``

SQLite & Other backends
    ``TEXT``


Installation
------------
::

    pip install django-stringfield


Usage
-----
You use this just like the normal ``django.db.models.CharField`` except that the
key word argument ``max_length`` works a little differently:

* It is optional and defaults to 500
* It only enforces max length on the default formfield **not** on the database.

Example::

    # models.py
    from stringfield import StringField

    class MyModel(models.Model):
        name = StringField()


.. [#f1] MySQL >= 5.0.3 should be able to handle a maximum length of 65535 but
    that does not work in my empirical testing using mysql 5.1.41 where 65528
    is the maximum considering ``NULL`` and ``NOT NULL``.

