#!/usr/bin/env python
import os
import sys
from django.conf import settings
from os.path import abspath, dirname, join as pjoin



def runtests(test_labels=None, verbosity=1, interactive=True, failfast=True):
    here = abspath(dirname(__file__))
    root = pjoin(here, os.pardir)
    sys.path[0:0] = [root, here]
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
    from django.test.utils import get_runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=verbosity, interactive=interactive, failfast=failfast)
    return test_runner.run_tests(test_labels)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Runs the test suite for django-stringfield.')
    parser.add_argument(
        'test_labels',
        nargs='*',
        help='Test labels.',
        )
    parser.add_argument(
        '--noinput',
        dest='interactive',
        action='store_false',
        default=True,
        help='Do not prompt the user for input of any kind.',
        )
    parser.add_argument(
        '--failfast',
        dest='failfast',
        action='store_true',
        default=False,
        help='Stop running the test suite after first failed test.',
    )
    args = parser.parse_args()
    failures = runtests(
        test_labels=args.test_labels,
        verbosity=1,
        interactive=args.interactive,
        failfast=args.failfast
        )
    if failures:
        sys.exit(bool(failures))

