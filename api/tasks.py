import decimal
import string
from datetime import time

from celery import shared_task
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
import requests
import re
from time import sleep

from bs4 import BeautifulSoup
from django.utils import timezone

from api.models import MovieDetails


def string_to_decimal(str_decimal):
    return decimal.Decimal(str_decimal)


def duration_to_time(duration):
    time_list = duration.replace("h", "").replace("min", "").split()
    return time(int(time_list[0]), int(time_list[1]), 0)


def string_date(string_date):
    date_str = " ".join(string_date.split()[:3])
    print(timezone.datetime.strptime(date_str, "%d %B %Y"))
    return timezone.datetime.strptime(date_str, "%d %B %Y")


def clean_string(str_data):
    cleaned_string = re.sub(' +', ' ', str_data)
    cleaned_string = re.sub(r"(\n)\1{2,}", "", cleaned_string).strip()
    return cleaned_string


def get_movie_by_url(url="/title/tt0111161/"):
    sleep(2)
    page = requests.get(IMDB_BASE_URL + url)
    soup = BeautifulSoup(page.content, 'html.parser')
    subtext = soup.find('div', {"class": "subtext"})
    return {"duration": duration_to_time(clean_string(subtext.find('time').contents[0])),
            "release_date": string_date(
                soup.find('div', {"class": "subtext"}).findAll('a', {'title': 'See more release dates'})[0].contents[
                    0]),
            "description": soup.find('div', {"class": ['summary_text', 'ready']}).contents[0]}


IMDB_BASE_URL = "https://www.imdb.com"


@shared_task
def get_movie_and_insert():
    page = requests.get(IMDB_BASE_URL + "/chart/top?ref_=nv_mv_250")
    soup = BeautifulSoup(page.content, 'html.parser')
    result_list = list()
    for div in soup.select('tbody tr'):
        item_dict = {"tittle": div.find('td', {'class': "titleColumn"}).find('a').contents[0],

                     "year": str(div.find('td', {'class': "titleColumn"}).find('span').contents[0]),
                     "rating": string_to_decimal(
                         div.find('td', {'class': "ratingColumn imdbRating"}).find('strong').contents[0])}
        sleep(2)
        item_dict.update(get_movie_by_url(div.find('td', {'class': "titleColumn"}).find('a')['href']))
        print(item_dict)
        MovieDetails.objects.create(name=item_dict.get('tittle'), release_date=item_dict.get('release_date'),
                                    duration=item_dict.get('duration'), ratings=item_dict.get("rating"),
                                    description=item_dict.get('description'))
