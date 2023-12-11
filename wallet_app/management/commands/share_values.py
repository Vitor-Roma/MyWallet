from django.core.management.base import BaseCommand
from wallet_app.models import Share
from wallet_app.utils.webscrapping_fiis import fiis_value
from wallet_app.utils.get_driver import get_driver


class Command(BaseCommand):

    def handle(self, *args, **options):
        fiis_value([share for share in Share.objects.filter(type='Fundos Imobiliarios')], get_driver())
