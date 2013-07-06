# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from unittest import TestCase
from pytypes.ast import ClassType, ParameterizedType, TextRange, TextPosition
from pytypes.parser import parse, make_range


class ParserTest(TestCase):
    def test_class_type(self):
        self.assertEqual(parse('int'),
                         ClassType('int',
                                   make_range((1, 1), (1, 3))))
        self.assertEqual(parse('collections.Iterable'),
                         ClassType('collections.Iterable',
                                   make_range((1, 1), (1, 20))))

    def test_param_type(self):
        self.assertEqual(parse('list of int'),
                         ParameterizedType(
                             ClassType('list'),
                             [ClassType('int')]))
        self.assertEqual(parse('dict of (str, int)'),
                         ParameterizedType(
                             ClassType('dict'),
                             [ClassType('str'), ClassType('int')]))

    def test_bracket_param_type(self):
        self.assertEqual(parse('list[int]'),
                         ParameterizedType(
                             ClassType('list'),
                             [ClassType('int')]))
        self.assertEqual(parse('dict[str, int]'),
                         ParameterizedType(
                             ClassType('dict'),
                             [ClassType('str'), ClassType('int')]))

