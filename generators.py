import math
import random

MAX_INTEGER = 9223372036854775807
MIN_INTEGER = -9223372036854775808


def generate_integer(multiple_of=1,
                     maximum=MAX_INTEGER,
                     exclusive_maximum=MAX_INTEGER,
                     minimum=MIN_INTEGER,
                     exclusive_minimum=MIN_INTEGER):
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
                    exclusive_minimum=MIN_INTEGER):
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


def generate_boolean():
    return random.choice([True, False])
