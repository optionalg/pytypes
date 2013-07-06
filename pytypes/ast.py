# -*- coding: utf-8 -*-

# Copyright 2013 JetBrains s.r.o.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.


"""Abstract syntax tree of Python types."""


from __future__ import unicode_literals
from collections import Sequence, namedtuple


class Type(object):
    """Base class for Python types."""
    pass


class ClassType(Type):
    """Simple class type.

    :type name: unicode
    :type range: TextRange or None
    """

    def __init__(self, name, range=None):
        self.name = name
        self.range = range

    def __eq__(self, other):
        return (isinstance(other, ClassType) and
                self.name == other.name and
                (self.range is None or other.range is None or
                 self.range == other.range))

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return 'ClassType({!r}, {!r})'.format(self.name, self.range)


class ParameterizedType(Type, namedtuple('ParameterizedType',
                                         'type parameters')):
    """Type with parameters.

    :type type: Type
    :type parameters: Sequence of Type
    """
    pass


class TypeParameter(Type, namedtuple('TypeParameter', 'name bound')):
    """Polymorphic type parameter.

    The upper bound may be None.

    :type name: unicode
    :type bound: Type
    """
    pass


class CallableType(Type, namedtuple('CallableType',
                                    'arguments star_args kwargs result')):
    """Callable type.

    :type arguments: Sequence of Type
    :type star_args: Type
    :type kwargs: Type
    :type result: Type
    """
    pass


class UnionType(Type, namedtuple('UnionType', 'types')):
    """Union of types.

    :type types: Sequence of Type
    """
    pass


class LiteralType(Type, namedtuple('LiteralType', 'value')):
    """Literal instance type.

    Allowed literals: None, booleans, integers, floats, bytes, unicode.

    :type value: unicode
    """
    pass


class NullableType(Type, namedtuple('NullableType', 'type')):
    """Type or None.

    Redundant: can be expressed as UnionType([type, LiteralType("None")]).

    :type type: Type
    """
    pass


class TextPosition(namedtuple('TextPosition', 'line column')):
    """Position in text.

    Lines and columns are 1-based.

    :type line: int
    :type column: int
    """
    pass


class TextRange(namedtuple('TextRange', 'start end')):
    """Text range.

    :type start: TextPosition
    :type end: TextRange
    """
    pass
