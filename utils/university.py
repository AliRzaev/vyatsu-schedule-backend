import requests

GROUPS_INFO_URL = 'https://www.vyatsu.ru/studentu-1/spravochnaya-informatsiya' \
                  '/raspisanie-zanyatiy-dlya-studentov.html'

DEPARTMENTS_INFO_URL = 'https://www.vyatsu.ru/studentu-1/' \
                       'spravochnaya-informatsiya/teacher.html'


def get_groups_page() -> str:
    response = requests.get(GROUPS_INFO_URL)
    return response.text


def get_departments_page() -> str:
    response = requests.get(DEPARTMENTS_INFO_URL)
    return response.text
