def sum_even_numbers(numbers):
    """Return the sum of only the even numbers in the given list.

    Args:
        numbers: A list of numbers (ints or floats).

    Returns:
        The sum of the even numbers. Returns 0 if there are none.
    """
    return sum(n for n in numbers if n % 2 == 0)
