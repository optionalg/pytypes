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

"""Python type annotations.

TODO
"""

from __future__ import unicode_literals
from collections import Sequence


class Type(object):
    """Base class for Python types."""
    pass


class ClassType(Type):
    """Simple class type.

    :type name: str or unicode
    """

    def __init__(self, name):
        self.name = name


class ParameterizedType(Type):
    """Type with parameters.

    :type type: Type
    :type parameters: Sequence of Type
    """

    def __init__(self, type, parameters):
        self.type = type
        self.parameters = parameters


class TypeParameter(Type):
    """Polymorphic type parameter.

    The upper bound may be None.

    :type name: str or unicode
    :type bound: Type
    """

    def __init__(self, name, bound):
        self.name = name
        self.bound = bound


class CallableType(Type):
    """Callable type.

    :type arguments: Sequence of Type
    :type star_args: Type
    :type kwargs: Type
    :type result: Type
    """

    def __init__(self, arguments, star_args, kwargs, result):
        self.arguments = arguments
        self.star_args = star_args
        self.kwargs = kwargs
        self.result = result


class UnionType(Type):
    """Union of types.

    :type types: Sequence of Type
    """

    def __init__(self, types):
        self.types = types


class LiteralType(Type):
    """Literal instance type.

    Allowed literals: None, booleans, integers, floats, bytes, unicode.

    :type value: str or unicode
    """

    def __init__(self, value):
        self.value = value


class NullableType(Type):
    """Type or None.

    Redundant: can be expressed as UnionType([type, LiteralType("None")]).

    :type type: Type
    """

    def __init__(self, type):
        self.type = type
