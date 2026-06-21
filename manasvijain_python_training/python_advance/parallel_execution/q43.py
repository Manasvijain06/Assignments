# Question 43 :  Demonstrate the use of join() method in threading.

"""
join() is used to make the main thread wait for another thread to complete its execution before continuing. 
It helps synchronize threads and ensures tasks finish in the desired order.
"""

import threading
import time


def perform_task() -> None:
    """
    Returns: None
    """
    print("Task Started")

    time.sleep(3)

    print("Task Completed")


if __name__ == "__main__":
    worker_thread = threading.Thread(target=perform_task)

    worker_thread.start()

    worker_thread.join()

    print("Main thread resumed after join().")