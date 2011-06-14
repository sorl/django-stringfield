from django.conf import settings
from django.core.management.color import no_style
from django.core.management.sql import sql_all
from django.db import connections
from django.db import models
from django.test import TestCase
from .models import Item


ALIAS = settings.DATABASES.keys()


sqlite_sql = """CREATE TABLE "stringfield_tests_item" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" TEXT NOT NULL
)
;"""

postgresql_sql = """CREATE TABLE "stringfield_tests_item" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" character varying NOT NULL
)
;"""


mysql_sql = """CREATE TABLE `stringfield_tests_item` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` VARCHAR (65528) NOT NULL
)
;"""

ALIAS_SQL = {}
for j, sql in enumerate([sqlite_sql, postgresql_sql, mysql_sql]):
    try:
        ALIAS_SQL[ALIAS[j]] = sql
    except IndexError:
        break


class SimpleTestCase(TestCase):
    def test_sql(self):
        for alias in ALIAS:
            self.assertEqual(
                ALIAS_SQL[alias],
                u'\n'.join(sql_all(models.get_app('stringfield_tests'), no_style(), connections[alias])),
                )

    def test_long_string(self):
        for alias in ALIAS:
            s = ''.join(['a' for j in xrange(0, 65000)])
            item = Item(name=s)
            item.save(using=alias)

