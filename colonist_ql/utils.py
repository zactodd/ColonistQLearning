import numpy as np
import time
import cv2


def distance(a, b):
    return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def contour_bounding_box(image, contour):
    """
    Gets a sub image base on a contour.
    :param image: THe image to obtain the sub image from.
    :param contour: The contour to base the sub image on.
    :return: The sub image.
    """
    x, y, w, h = cv2.boundingRect(contour)
    return image[y:y + h, x:x + w]


def calculate_run_time(func):
    """
    Calculates the run time of a function.
    :param func: The function to calculate the run time of.
    :return: The decorator for the function.
    """
    def inner(*args, **kwargs):
        print(f"Starting {func.__name__}")
        start = time.time()
        func(*args, **kwargs)
        print(f"Total time taken in: {func.__name__} {start - time.time()}")
    return inner
