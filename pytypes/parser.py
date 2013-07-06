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
from functools import wraps
from funcparserlib.lexer import make_tokenizer
from funcparserlib.parser import finished, many, some, skip
from pytypes.ast import ClassType


__all__ = ['parse']

token_specs = [
    ('space', (r'[ \t\r\n]+',)),
    ('identifier', (r'[A-Za-z_][A-Za-z_0-9]*',)),
    ('op', (r'\.',)),
]


def tok(type, name=None):
    """Parse a single token.

    :type type: unicode
    :type name: unicode or None
    """
    return (some(lambda t: t.type == type and (name is None or t.name == name))
            >> (lambda t: t.value))


def op(name):
    """Parse an operator token.

    :type name: unicode
    """
    return skip(tok('op', name))


def star_args(f):
    @wraps(f)
    def wrapper(args):
        return f(*args)
    return wrapper


@star_args
def make_class_type(id, ids):
    """Create a ClassType from parse results.

    :type id: unicode
    :type ids: list of unicode
    """
    return ClassType('.'.join([id] + ids))


identifier = tok('identifier')
class_type = identifier + many(op('.') + identifier) >> make_class_type
type_expr = class_type
type_file = type_expr + skip(finished)


def tokenize(s):
    """Tokenize a type string.

    :type s: unicode
    """
    f = make_tokenizer(token_specs)
    return [t for t in f(s) if t.type != 'space']


def parse(s):
    """Parse a type string.

    :type s: unicode
    """
    return type_file.parse(tokenize(s))
