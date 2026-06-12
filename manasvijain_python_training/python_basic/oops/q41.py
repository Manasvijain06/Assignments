"""Question 41 : Create a Car class with a constructor."""

class Car:
    """ Represent a car."""

    def __init__(self,brand: str,model: str) -> None:
        """Initialize car attributes."""

        self.brand = brand
        self.model = model

    def display_details(self) -> None:
        """Display car details."""
        
        print(f"Brand: {self.brand}")
        print(f"Model: {self.model}")

if __name__ == "__main__":
    car = Car("Toyota", "Camry")
    car.display_details()