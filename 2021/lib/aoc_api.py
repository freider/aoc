import os
import requests


def env_session():
    return os.environ["AOC_SESSION_ID"]


class Aoc:
    def __init__(self, session_id=None):
        if session_id is None:
            session_id = env_session()
        self.session_id = session_id

    def fetch_input(self, year, day):
        return requests.get(f"https://adventofcode.com/{year}/day/{day}/input", cookies={"session": self.session_id}).text


if __name__ == "__main__":
    print(Aoc().fetch_input(2018, 15))
