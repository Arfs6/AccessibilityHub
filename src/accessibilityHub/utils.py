# -*- coding: utf-8 -*-
"""This module contains utility functions"""


BASE36VALUES = '0123456789abcdefghijklmnopqrstuvwxyz'


def decimal2Base36(decimal: int) -> str:
    """Converts a decimal integer to base 36.
    parameters:
    - decimal: The number to convert to base 36
    Returns: The base36 equivalent of the number.
    """
    intToBase36Values = {i: BASE36VALUES[i] for i in range(36)}
    base36 = ''
    while True:  # stop when quotient is zero.
        quotient, remainder = divmod(decimal, 36)
        base36 += intToBase36Values[remainder]
        if quotient == 0:
            break
        decimal = quotient
    return base36[::-1]


def base362Decimal(base36: str) -> int:
    """Converts a base36 number to decimal (base 10).
    parameters:
    - base36: base 36 based number to convert.
    returns: int equivalent of provided base36 number.
    """
    base36ToIntValues = {base36: dec for dec, base36 in enumerate(BASE36VALUES)}
    base36 = base36[::-1]
    return sum([base36ToIntValues[b] * (36 ** i) for i, b in enumerate(base36)])
