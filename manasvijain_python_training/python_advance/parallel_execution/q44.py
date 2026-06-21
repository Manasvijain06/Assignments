# Question 44 :  Create multiple threads to simulate file downloading using time.sleep().

import threading
import time

# CONSTANTS
DOWNLOAD_TIME: int = 2


def download_file(file_name: str) -> None:
    """
    Simulate downloading a file.

    Args:
        file_name: Name of the file.
    """
    print(f"Downloading {file_name}...")

    time.sleep(DOWNLOAD_TIME)

    print(f"{file_name} downloaded.")


if __name__ == "__main__":
    thread_1 = threading.Thread(target=download_file, args=("File1.pdf",))

    thread_2 = threading.Thread(target=download_file, args=("File2.pdf",))

    thread_3 = threading.Thread(target=download_file, args=("File3.pdf",))

    thread_1.start()
    thread_2.start()
    thread_3.start()

    thread_1.join()
    thread_2.join()
    thread_3.join()

    print("All downloads completed.")