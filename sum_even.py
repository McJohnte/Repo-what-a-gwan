def sum_even_numbers(numbers):
    if not isinstance(numbers, list):
        raise TypeError(f"Expected a list, got {type(numbers).__name__}")
    for i, n in enumerate(numbers):
        if not isinstance(n, (int, float)) or isinstance(n, bool):
            raise TypeError(f"Element at index {i} is not a number: {n!r}")
    return sum(n for n in numbers if n % 2 == 0)
