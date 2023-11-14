from math import ceil
from random import choice, randint
from time import sleep

import pyautogui as pg
import pyperclip
from bs4 import BeautifulSoup

from config import CONFIG


class Visitor:
    def __init__(self):
        self._search_url = "https://www.google.com"
        self._solution = (1920, 1080)

    def _check_key_words(self, key_words_row):
        if len(key_words_row) == 0:
            pg.alert(
                text="Key words row is empty.\nCorrect configuration file",
                title="Error",
                button="OK",
            )
            pg.hotkey("ctrl", "w")
            exit()

        return key_words_row.split(";")

    def _check_url(self, url):
        if len(url) == 0:
            pg.alert(
                text="Find url is empty.\nCorrect configuration file",
                title="Error",
                button="OK",
            )
            pg.hotkey("ctrl", "w")
            exit()

    def _get_links(self):
        pyperclip.copy("")

        pg.hotkey("ctrl", "u")
        sleep(4)

        pg.hotkey("ctrl", "a")
        pg.hotkey("ctrl", "c")
        sleep(2)

        html_data = pyperclip.paste()
        sleep(2)

        pg.hotkey("ctrl", "w")

        soup = BeautifulSoup(html_data, "html.parser")

        filters = soup.find_all("h3", class_="LC20lb MBeuO DKV0Md")

        if len(filters) == 0:
            pg.alert(
                text="No links were found\nTry one more time",
                title="Error",
                button="OK",
            )
            pg.hotkey("ctrl", "w")
            exit()

        links = [
            f.parent.contents[2].contents[1].contents[1].get_text().split(" › ")[0]
            for f in filters
        ]

        return links

    def _get_wait_time(self):
        return randint(10, 30) / 100

    def _open_browser(self):
        pg.hotkey("winleft")
        sleep(2)

        pg.typewrite("https://www.google.com\n", self._get_wait_time())
        sleep(2)

    def _scrolling(self, seconds):
        while seconds > 0:
            action = randint(-1, 1)

            if action != 0:
                scroll_value = randint(100, 1_000)
                scroll_step = randint(15, 30)
                while scroll_value > 0:
                    pg.scroll(action * scroll_step)
                    sleep(self._get_wait_time() / 10)

                    scroll_value -= scroll_step
                seconds -= 1

            else:
                sleep_time = randint(1, ceil(seconds / 5))
                sleep(sleep_time)
                seconds -= sleep_time

    def _search(self, key_word):
        pg.typewrite(f"{key_word}\n", self._get_wait_time())
        sleep(2)

        pg.hotkey("ctrl", "l")
        pg.press("right")
        pg.typewrite(f"&num={CONFIG['search_limit']}\n", self._get_wait_time())
        sleep(2)

        links = self._get_links()
        unimportant_site_count = randint(
            CONFIG["unimportant_site_count_from"], CONFIG["unimportant_site_count_to"]
        )

        for _ in range(unimportant_site_count):
            visit_url = choice(links)
            self._visit_site(
                visit_url,
                CONFIG["unimportant_site_scrolling_from"],
                CONFIG["unimportant_site_scrolling_to"],
            )

        if CONFIG["find_url"] in links:
            self._visit_site(
                CONFIG["find_url"],
                CONFIG["important_site_scrolling_from"],
                CONFIG["important_site_scrolling_to"],
            )

            return 1

        return 0

    def _visit_site(self, url, scrolling_from, scrolling_to):
        pg.hotkey("ctrl", "f")
        pg.typewrite(f"{url}\n", self._get_wait_time())
        pg.press("escape")
        sleep(1)

        pg.press("enter")
        sleep(3)

        self._scrolling(randint(scrolling_from, scrolling_to))
        pg.hotkey("alt", "left")
        sleep(2)

    def run(self):
        pg.alert(text="Change language to english", title="Info", button="OK")

        key_words = self._check_key_words(CONFIG["key_words"])
        self._check_url(CONFIG["find_url"])

        self._open_browser()

        while len(key_words) > 0:
            current_key_word = key_words.pop(randint(0, len(key_words) - 1))

            result = self._search(current_key_word)

            if result:
                sleep(2)
                break

            pg.press("home")

            logo_position = pg.locateCenterOnScreen("logo.png", confidence=0.8)

            if logo_position is None:
                pg.alert(
                    text="Google logo not found\nTry one more time",
                    title="error",
                    button="OK",
                )
                pg.hotkey("ctrl", "w")
                exit()
            else:
                pg.moveTo(*logo_position, duration=self._get_wait_time())
                pg.click()
                sleep(2)

        pg.hotkey("ctrl", "w")


visitor = Visitor()
visitor.run()
