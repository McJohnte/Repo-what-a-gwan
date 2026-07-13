def is_armstrong(number):
    digits = str(number)
    power = len(digits)
    return number == sum(int(digit) ** power for digit in digits)


if __name__ == "__main__":
    number = int(input("Enter a number: "))
    if is_armstrong(number):
        print(f"{number} is an Armstrong number")
    else:
        print(f"{number} is not an Armstrong number")
