import sys
import os
import time
import cv2
import numpy as np
from PIL import ImageGrab
from colonist_ql import exceptions
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import pygetwindow as gw


def game_image():
    """
    Obtains a screenshot of the current game state.
    :return: image of the game.
    :raise: if there is no game raise exceptions.GameNotFoundException()
    """
    current_window = gw.getActiveWindow()
    for title in gw.getAllTitles():
        if "Colonist: Play" in title:
            game_window = gw.getWindowsWithTitle(title)[0]
            game_window.minimize()
            game_window.maximize()
            time.sleep(0.4)

            # Screen capture
            image = ImageGrab.grab()
            image = np.array(image)

            # Removing boarder
            h, w, *_ = image.shape
            image = image[10:h - 10, 10: w - 10]

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            game_window.minimize()
            current_window.maximize()
            return image
    else:
        raise exceptions.GameNotFoundException()


def game_images(wait=0.25):
    """
    Yields a continuous stream of game images at a specified interval.
    :param wait: wait time in seconds.
    :yield:
    """
    while True:
        try:
            yield game_image()
        except exceptions.GameNotFoundException as e:
            print("Game Not Found.")
        time.sleep(wait)


def get_chrome_driver():
    """
    Installs the chrome driver if already installed gets the drivers path.
    :return: The driver.
    """
    sys.stdout = open(os.devnull, 'w')
    try:
        path = ChromeDriverManager().install()
    except PermissionError as e:
        if e.errno != 13:
            raise e
        path = e.filename
    finally:
        sys.stdout = sys.__stdout__
    return webdriver.Chrome(path)


def log_game_images(log_dir, log_name_func, wait=0.25):
    """
    Logs game image to a directory.
    :param log_dir: The directory of the log file.
    :param log_name_func: A function that creates constance log names.
    :param wait: Wait time between image captures.
    """
    for i in game_images(wait):
        print(f"Logging: {log_dir}/{log_name_func()}.png")
        cv2.imwrite(f"{log_dir}/{log_name_func()}.png", i)


def time_format():
    return datetime.now().strftime("%Y_%m_%d__%H_%M_%S")


