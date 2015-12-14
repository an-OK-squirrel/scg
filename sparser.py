# coding: utf-8

import re

L_LETTERS = 'abcdefghijklmnopqrstuvwxyz'
U_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
DIGITS = '0123456789'
ALL_LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
OPERATORS = L_LETTERS + '+*/-=^;[]@\\~!%'
WHITESPACE = ' \t'


def does_regex_match(regex, string):
    thing = re.match(regex, string)
    try:
        return str(thing) is not None and thing.group() == string
    except AttributeError:
        return False


def split_into_st(program):
    # split_into_st('apple')
    # ['a', 'p', 'p', 'l', 'e']
    result = []
    char_index = 0
    token_type = 0  # 0 is none, 1 is op, 2 is num, 3 is string
    # 4 is block, 5 is setvar.
    token = ''

    while char_index < len(program):
        char = program[char_index]
        if token_type == 0:  # Token is empty
            if char in WHITESPACE:  # Y U whitespace in codegolf?
                token = ''
                token_type = 0
            elif char in OPERATORS:  # Do things
                token += char
                token_type = 1
                result.append([token, token_type])
                token = ''  # reset
                token_type = 0
            elif char == '.' or char == '°':
                token += '.'
                token_type = 1
            elif char in DIGITS:
                token += char
                token_type = 2
            elif char == '"':
                token_type = 3
                token = '"'
            elif char == '{':
                token_type = 4
                token = '{'
            elif char == ':':
                token_type = 5
                token = ':'
        elif token_type == 1 or token_type == 5:
            token += char
            result.append([token, token_type])
            token = ''
            token_type = 0
        elif token_type == 2:
            if char in DIGITS:
                token += char
            elif char == '.':
                pass  # token += char
            else:
                result.append([token, token_type])
                token = ''
                token_type = 0
                char_index -= 1
        elif token_type == 3:
            if char == '"':
                result.append([token, token_type])  # We don't want "abc",
                # rather "abc
                token = ''
                token_type = 0
            else:
                token += char
        elif token_type == 4:
            if char == '}':
                result.append([token, token_type])  # We don't want {123},
                # rather {123
                token = ''
                token_type = 0
            else:
                token += char

        char_index += 1
    result.append([token, token_type])
    return result

types = ['none', 'operator', '.operator']


def parse_token_st(tokens):
    result = []
    for token in tokens:
        token_type = token[1]
        if token_type == 0:
            pass
        elif token_type == 1:
            result.append({'token_type': 'operator', 'token_value': token[0]})
        elif token_type == 2:
            result.append({'token_type': 'integer',
                          'token_value': int(token[0])})
        elif token_type == 3:
            result.append({'token_type': 'string',
                          'token_value': str(token[0][1:])})
        elif token_type == 4:
            result.append({'token_type': 'block',
                          'token_value': parse_token_st(
                          split_into_st(token[0][1:]))})
        elif token_type == 5:
            result.append({'token_type': 'setvar', 'token_value': token[0]})
    return result

replace_chars = {
    'à': ' 0',
    'á': ' 1',
    'â': ' 2',
    'ã': ' 3',
    'ä': ' 4',
    'å': ' 5',
    'æ': ' 6',
    'ç': ' 7',
    'è': ' 8',
    'é': ' 9',
}


def char_replace(code):
    result = ""
    for char in code:
        if char in replace_chars:
            result += replace_chars[char]
        else:
            result += char

    return result


def fully_parse(code):
    return parse_token_st(split_into_st(char_replace(code)))
