from bs4 import BeautifulSoup


def convert_to_soup(response):
    return BeautifulSoup(response.text, "lxml")
