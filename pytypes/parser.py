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
from funcparserlib.lexer import make_tokenizer, Token
from funcparserlib.parser import finished, many, some, skip, forward_decl
from pytypes.ast import ClassType, ParameterizedType, TextRange, TextPosition


__all__ = ['parse']

token_specs = [
    ('space', (r'[ \t\r\n]+',)),
    ('op', (r'[\.,\(\)\[\]]|(of)',)),
    ('identifier', (r'[A-Za-z_][A-Za-z_0-9]*',)),
]


def tok(type, name=None):
    """Parse a single token.

    :type type: unicode
    :type name: unicode or None
    """
    return some(lambda t: t.type == type and (name is None or t.name == name))


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


def make_range(start, end):
    line1, col1 = start
    line2, col2 = end
    return TextRange(TextPosition(line1, col1), TextPosition(line2, col2))


@star_args
def make_class_type(head, tail):
    """Create a ClassType from parse results.

    :type head: Token
    :type tail: list of Token
    """
    tokens = [head] + tail
    return ClassType('.'.join([t.value for t in tokens]),
                     make_range(tokens[0].start, tokens[-1].end))


@star_args
def make_param_type(type, param):
    params = param if isinstance(param, list) else [param]
    return ParameterizedType(type, params)


@star_args
def make_param_list(head, tail):
    return [head] + tail


identifier = tok('identifier')
class_type = identifier + many(op('.') + identifier) >> make_class_type
type_expr = forward_decl()
simple_expr = class_type
paren_param_list = (
    op('(') + type_expr + many(op(',') + type_expr) + op(')')
    >> make_param_list)
bracket_param_list = (
    op('[') + type_expr + many(op(',') + type_expr) + op(']')
    >> make_param_list)
of_param_list = op('of') + (paren_param_list | type_expr)
param_type = (
    simple_expr + (of_param_list | bracket_param_list)
    >> make_param_type)
type_expr.define(param_type | class_type)
type_file = type_expr + skip(finished)


def name_parser_vars(vars):
    for k, v in vars.items():
        if hasattr(v, 'named'):
            v.named(k)


name_parser_vars(globals())


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
