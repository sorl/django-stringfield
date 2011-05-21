#!/usr/bin/env python
import os
import sys
from os.path import abspath, dirname, join as pjoin
from django.conf import settings


def runtests(*test_labels):
    here = abspath(dirname(__file__))
    root = pjoin(here, os.pardir)
    sys.path.append(root)
    sys.path.append(here)
    labels = ['stringfield', 'stringfield_tests']
    test_labels = test_labels or labels
    if not settings.configured:
        settings.configure(
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                },
                'postgresql': {
                    'ENGINE': 'django.db.backends.postgresql_psycopg2',
                    'NAME': 'stringfield',
                },
                'mysql': {
                    'ENGINE': 'django.db.backends.mysql',
                    'NAME': 'stringfield',
                },
            },
            INSTALLED_APPS=labels,
        )
    from django.test.simple import DjangoTestSuiteRunner
    runner = DjangoTestSuiteRunner()
    return runner.run_tests(test_labels)


if __name__ == '__main__':
    failures = runtests(*sys.argv[1:])
    sys.exit(failures)

