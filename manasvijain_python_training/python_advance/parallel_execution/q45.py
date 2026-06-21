# Question 45 :  Write a program to create two processes that print their Process IDs.

import multiprocessing
import os


def print_process_id(process_name: str) -> None:
    """
    Print Process ID.
    """
    print(f"process_id: {os.getpid()}")


if __name__ == "__main__":
    process_1 = multiprocessing.Process(target=print_process_id, args=("Process 1",))

    process_2 = multiprocessing.Process(target=print_process_id, args=("Process 2",))

    process_1.start()
    process_2.start()

    process_1.join()
    process_2.join()

    print("Both processes completed.")