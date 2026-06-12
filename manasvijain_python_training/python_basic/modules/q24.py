"""question 24 : Create your own module and import it."""

from own_module import hello_user

if __name__ == "__main__":
    name = input("Enter your name: ")
    message = hello_user(name)
    print(message)