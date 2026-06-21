# Question 15 : Write a program that processes a large dataset using a generator instead of storing all values in a list.

# CONSTANTS
LIMIT: int = 1_000_000

def generator_number(limit: int):
    """
    Generate numbers from 1 to n.

    Args:
        limit: Upper limit.

    Yields:
        int: Next number.
    """
    for number in range(1, limit + 1):
        yield number


def process_dataset(limit: int) -> None:
    """
    Process dataset using generator without storing all values.

    Args:
        limit: Number of elements to process.
    """
    processed_records: int = 0

    for _ in generator_number(limit):
        processed_records += 1  # Simulating processing

    print(f"Processed {processed_records:,} records.")


if __name__ == "__main__":
    print("\n--- Large Dataset Processing Using Generator ---")
    process_dataset(LIMIT)