from numbers import Integral


def sum_even_numbers(numbers):
    """Return the sum of only the even numbers in the given list.

    Args:
        numbers: A list (or other iterable) of integer values.

    Returns:
        The sum of the even numbers. Returns 0 if there are none.

    Raises:
        TypeError: If ``numbers`` is not iterable, or if any element is not
            an integer (e.g. a float, string, or ``None``). Booleans are
            rejected as well, since they are not meaningful here even though
            Python treats them as a subtype of ``int``.
    """
    try:
        items = list(numbers)
    except TypeError:
        raise TypeError(
            f"expected an iterable of integers, got {type(numbers).__name__}"
        )

    for n in items:
        if isinstance(n, bool) or not isinstance(n, Integral):
            raise TypeError(
                f"all elements must be integers, got {n!r} "
                f"of type {type(n).__name__}"
            )

    return sum(n for n in items if n % 2 == 0)
