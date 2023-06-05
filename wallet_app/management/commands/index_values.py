from django.core.management.base import BaseCommand
from wallet_app.utils.webscrapping_indices import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        get_IPCA()
        get_dolar_and_euro()
        get_CDI_and_Selic()
        get_BITCOIN_and_ETHEREUM()
