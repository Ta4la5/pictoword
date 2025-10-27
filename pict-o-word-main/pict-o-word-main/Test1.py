for num in range (0, 1001):
    if (num % 5 == 0) and (num % 3 == 0):
        print("Fizzbuzz")
    elif num % 5 == 0:
        print("Buzz")
    elif num % 3 == 0:
        print("Fizz")
    else:
        print(num)