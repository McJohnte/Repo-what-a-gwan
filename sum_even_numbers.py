def sum_even_numbers(numbers):
    if not isinstance(numbers, list):
        raise TypeError(f"Expected a list, got {type(numbers).__name__}")
    validated = []
    for n in numbers:
        if not isinstance(n, (int, float)) or isinstance(n, bool):
            raise TypeError(f"All elements must be numeric, got {type(n).__name__}: {n!r}")
        validated.append(n)
    return sum(n for n in validated if n % 2 == 0)
