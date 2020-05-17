from colonist_ql.interface_interaction.utils import get_chrome_driver

DRIVER = get_chrome_driver()
URL = "https://colonist.io/"


class Page:
    def __init__(self, url, browser=DRIVER):
        self.browser = self._browser_initialise(url, browser)

    @staticmethod
    def _browser_initialise(url, browser):
        """
        Initialise the browser.
        :param browser: The browser prior to being initialise.
        :return: The browser.
        """
        browser.get(url)
        return browser
