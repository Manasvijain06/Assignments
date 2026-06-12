"""Question 44 : Demonstrate polymorphism using different classes with the same method name."""

class Dog:

    def make_sound(self) -> None:
        """Display dog sound."""

        print("Dog barks.")


class Cat:

    def make_sound(self) -> None:
        """Display cat sound."""

        print("Cat meows.")


class Cow:

    def make_sound(self) -> None:
        """Display cow sound."""

        print("Cow moos.")

if __name__ == "__main__":
    dog = Dog()
    cat = Cat()
    cow = Cow()

    dog.make_sound()
    cat.make_sound()
    cow.make_sound()