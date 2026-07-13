def is_duck_number(number):
    digits = str(number)
    return digits[0] != "0" and "0" in digits[1:]


if __name__ == "__main__":
    number = input("Enter a number: ")
    if is_duck_number(number):
        print(f"{number} is a duck number")
    else:
        print(f"{number} is not a duck number")
