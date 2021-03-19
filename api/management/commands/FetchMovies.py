from django.core.management import BaseCommand

from api.tasks import  get_movie_and_insert


class Command(BaseCommand):
    def handle(self, *args, **options):
        get_movie_and_insert.delay()
