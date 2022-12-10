from django.core.management.base import BaseCommand

from wallet_app.models import Share
from wallet_app.utils.webscrapping_fiis import fiis_value


class Command(BaseCommand):

    def handle(self, *args, **options):
        fiis_value([share.name for share in Share.objects.all()])
