import unittest

from schemer import Schema, ValidationException
from schemer.schema_level_validators import requires_at_least_one_of, requires_exactly_one_of, requires_all_or_none_of, \
    mutually_exclusive


class TestRequiresAtLeastOneOf(unittest.TestCase):
    def setUp(self):
        self.schema = Schema({
            'somefield': {'type': str},
            'otherfield': {'type': str},
            'anotherfield': {'type': str},

        }, validates=requires_at_least_one_of('somefield', ['otherfield', 'anotherfield']))

    def test_valid(self):
        self.schema.validate({'somefield': 'somevalue'})
        self.schema.validate({'otherfield': 'othervalue', 'anotherfield': 'anothervalue'})
        self.schema.validate({'somefield': 'somevalue', 'otherfield': 'partialvalue'})
        self.schema.validate({'somefield': 'somevalue', 'otherfield': 'othervalue', 'anotherfield': 'anothervalue'})


    def test_invalid(self):
        with self.assertRaises(ValidationException):
             self.schema.validate({})

        with self.assertRaises(ValidationException):
             self.schema.validate({'otherfield': 'partialvalue'})


class TestRequiresExactlyOneOf(unittest.TestCase):
    def setUp(self):
        self.schema = Schema({
            'somefield': {'type': str},
            'otherfield': {'type': str},
            'anotherfield': {'type': str},

        }, validates=requires_exactly_one_of('somefield', ['otherfield', 'anotherfield']))

    def test_valid(self):
        self.schema.validate({'somefield': 'somevalue'})
        self.schema.validate({'somefield': 'somevalue', 'otherfield': 'partialvalue'})
        self.schema.validate({'otherfield': 'othervalue', 'anotherfield': 'anothervalue'})


    def test_invalid(self):
        with self.assertRaises(ValidationException):
             self.schema.validate({})

        with self.assertRaises(ValidationException):
             self.schema.validate({'otherfield': 'partialvalue'})

        with self.assertRaises(ValidationException):
             self.schema.validate({'somefield': 'somevalue', 'otherfield': 'othervalue', 'anotherfield': 'anothervalue'})


class TestRequiresAllOrNoneOf(unittest.TestCase):
    def setUp(self):
        self.schema = Schema({
            'somefield': {'type': str},
            'otherfield': {'type': str},
            'anotherfield': {'type': str},

        }, validates=requires_all_or_none_of('somefield', 'otherfield'))

    def test_valid(self):
        self.schema.validate({})
        self.schema.validate({'somefield': 'somevalue', 'otherfield': 'othervalue'})


    def test_invalid(self):
        with self.assertRaises(ValidationException):
             self.schema.validate({'otherfield': 'partialvalue'})


class TestMutuallyExclusive(unittest.TestCase):
    def setUp(self):
        self.schema = Schema({
            'somefield': {'type': str},
            'otherfield': {'type': str},
            'anotherfield': {'type': str},

        }, validates=mutually_exclusive('somefield', ['otherfield', 'anotherfield']))

    def test_valid(self):
        self.schema.validate({})
        self.schema.validate({'otherfield': 'partialvalue'})
        self.schema.validate({'somefield': 'somevalue'})
        self.schema.validate({'otherfield': 'othervalue', 'anotherfield': 'anothervalue'})
        self.schema.validate({'somefield': 'somevalue', 'otherfield': 'partialvalue'})


    def test_invalid(self):
        with self.assertRaises(ValidationException):
             self.schema.validate({'somefield': 'somevalue', 'otherfield': 'othervalue', 'anotherfield': 'anothervalue'})


