# Question 13 :  Write a generator expression to generate even numbers from 1 to 50.

def generate_even_number():
    """
    Return a generator expression for even numbers from 1 to 50.
    """
    return (number for number in range(1, 51) if number % 2 == 0)

if __name__ == "__main__":

    print("\n--- Even Number Generator ---")

    even_number = generate_even_number()

    for number in even_number:
        print(number)

