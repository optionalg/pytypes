# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from unittest import TestCase
from pytypes.ast import ClassType
from pytypes.parser import parse


class ParserTest(TestCase):
    def test_class_type(self):
        self.assertEqual(parse('int'),
                         ClassType('int'))
        self.assertEqual(parse('collections.Iterable'),
                         ClassType('collections.Iterable'))
