import math
import random
import re
import string

import exrex

MAX_INTEGER = 9223372036854775807
MIN_INTEGER = -9223372036854775808
MAX_STRLEN = 15
MIN_STRLEN = 0
CHARACTERS = string.ascii_letters + string.digits
MAX_ITEMS = 20
MIN_ITEMS = 0


def _camel_to_snake(s):
    t = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', t).lower()


def generate(schema):
    kwargs = {_camel_to_snake(k): v for k, v in schema.items()}
    if schema['type'] == 'null':
        return generate_null(**kwargs)
    if schema['type'] == 'boolean':
        return generate_boolean(**kwargs)
    if schema['type'] == 'integer':
        return generate_integer(**kwargs)
    if schema['type'] == 'number':
        return generate_number(**kwargs)
    if schema['type'] == 'string':
        return generate_string(**kwargs)
    if schema['type'] == 'array':
        return generate_array(**kwargs)
    if schema['type'] == 'object':
        return generate_object(**kwargs)


def generate_integer(multiple_of=1,
                     maximum=MAX_INTEGER,
                     exclusive_maximum=MAX_INTEGER,
                     minimum=MIN_INTEGER,
                     exclusive_minimum=MIN_INTEGER,
                     **kwargs):
    '''Generate valid random integer.

    Ref:
    https://json-schema.org/draft/2019-09/json-schema-validation.html#numeric

    Args:
        multiple_of (int): An integer is valid only if division by this
                           results in an integer. Should be an integer
                           strictly greater than 0.
        maximum (int): An inclusive upper limit for the integer.
        exclusive_maximum (int): An exclusive upper limit for the integer.
        minimum (int): An inclusive lower limit for the integer.
        exclusive_minimum (int): An exclusive lower limit for the integer.

    Returns:
        A valid random integer, or None if no valid output exists.

    '''
    maximum = min(maximum, exclusive_maximum - 1)
    minimum = max(minimum, exclusive_minimum + 1)
    if minimum > maximum:
        return None
    maximum = math.floor(maximum / multiple_of) * multiple_of
    minimum = math.ceil(minimum / multiple_of) * multiple_of
    if minimum > maximum:
        return None
    max_quotient = maximum // multiple_of
    min_quotient = minimum // multiple_of
    return multiple_of * random.randint(min_quotient, max_quotient)


def generate_number(multiple_of=None,
                    maximum=MAX_INTEGER,
                    exclusive_maximum=MAX_INTEGER,
                    minimum=MIN_INTEGER,
                    exclusive_minimum=MIN_INTEGER,
                    **kwargs):
    '''Generate valid random number.

    Ref:
    https://json-schema.org/draft/2019-09/json-schema-validation.html#numeric

    Args:
        multiple_of (int, float): A number is valid only if division by this
                                  results in an integer. Should be a number
                                  strictly greater than 0.
        maximum (int, float): An inclusive upper limit for the number.
        exclusive_maximum (int, float): An exclusive upper limit for
                                        the number.
        minimum (int, float): An inclusive lower limit for the number.
        exclusive_minimum (int, float): An exclusive lower limit for
                                        the number.

    Returns:
        A valid random number, or None if no valid output exists.

    '''
    if minimum > maximum:
        return None
    if exclusive_minimum >= exclusive_maximum:
        return None
    maximum = min(maximum, exclusive_maximum)
    minimum = max(minimum, exclusive_minimum)
    if minimum > maximum:
        return None
    if multiple_of is None:
        if minimum == maximum:
            return minimum
        number = random.uniform(minimum, maximum)
        while number >= exclusive_maximum or number <= exclusive_minimum:
            number = random.uniform(minimum, maximum)
        return number
    max_quotient = math.floor(maximum / multiple_of)
    min_quotient = math.ceil(minimum / multiple_of)
    maximum = max_quotient * multiple_of
    minimum = min_quotient * multiple_of
    if minimum > maximum:
        return None
    if minimum == maximum:
        if minimum <= exclusive_minimum or maximum >= exclusive_maximum:
            return None
        return minimum
    if minimum == exclusive_maximum:
        min_quotient += 1
    if maximum == exclusive_maximum:
        max_quotient -= 1
    number = multiple_of * random.randint(min_quotient, max_quotient)
    while number >= exclusive_maximum or number <= exclusive_minimum:
        number = multiple_of * random.randint(min_quotient, max_quotient)
    return number


def generate_boolean(**kwargs):
    return random.choice([True, False])


def generate_null(**kwargs):
    return None


def generate_string(max_length=MAX_STRLEN,
                    min_length=MIN_STRLEN,
                    pattern=None,
                    **kwargs):
    '''Generate a valid random string.

    Ref:
    https://json-schema.org/draft/2019-09/json-schema-validation.html#string

    Args:
        max_length (int): Upper limit of string length.
        min_length (int): Lowet limit of string length.
        pattern (str): A regular expression pattern.

    Returns:
        A valid random string.

    '''
    if pattern is not None:
        s = exrex.getone(pattern)
        if len(s) < min_length:
            s += ' ' * (min_length - len(s))
        if len(s) > max_length:
            s = s[:max_length]
        return s
    length = random.randint(min_length, max_length)
    return ''.join(random.choice(CHARACTERS) for _ in range(length))


def generate_array(items=[],
                   max_items=MAX_ITEMS,
                   min_items=MIN_ITEMS,
                   unique_items=False,
                   **kwargs):
    if len(items) == 1:
        schema = items[0]
        count = random.randint(min_items, max_items)
        if not unique_items:
            return [generate(schema) for _ in range(count)]
        existed = set()
        array = []
        while len(array) < count:
            item = generate(schema)
            if item not in existed:
                array.append(item)
                existed.add(item)
        return array
    return [generate(schema) for schema in items]


def generate_object(properties=[],
                    max_properties=None,
                    min_properties=None,
                    required=None,
                    dependent_required=None,
                    **kwargs):
    return {k: generate(v) for k, v in properties.items()}


if __name__ == '__main__':
    print(generate({
        "type": "object",
        "properties": {
            "dimensions": {
                "type": "object",
                "properties": {
                    "length": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 40
                    },
                    "width": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 30
                    },
                    "height": {
                        "type": "number",
                        "minimum": 10,
                        "maximum": 20
                    }
                },
                "required": ["length", "width", "height"]
            }
        }
    }))
