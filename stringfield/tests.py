from stringfield import StringField
from django.core.exceptions import ValidationError
from django.test import TestCase


class ValidationTest(TestCase):
    def test_stringfield_raises_error_on_empty_string(self):
        f = StringField()
        self.assertEqual('', f.clean('', None))

    def test_stringfield_cleans_empty_string_when_blank_true(self):
        f = StringField(blank=False)
        self.assertRaises(ValidationError, f.clean, "", None)

    def test_stringfield_with_choices_cleans_valid_choice(self):
        f = StringField(max_length=1, choices=[('a','A'), ('b','B')])
        self.assertEqual('a', f.clean('a', None))

    def test_stringfield_with_choices_raises_error_on_invalid_choice(self):
        f = StringField(choices=[('a','A'), ('b','B')])
        self.assertRaises(ValidationError, f.clean, "not a", None)

    def test_stringfield_raises_error_on_empty_input(self):
        f = StringField(null=False)
        self.assertRaises(ValidationError, f.clean, None, None)

