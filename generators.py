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
