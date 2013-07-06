# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from unittest import TestCase
from pytypes.ast import ClassType, ParameterizedType
from pytypes.parser import parse


class ParserTest(TestCase):
    def test_class_type(self):
        self.assertEqual(parse('int'),
                         ClassType('int'))
        self.assertEqual(parse('collections.Iterable'),
                         ClassType('collections.Iterable'))

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
