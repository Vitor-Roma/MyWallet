from django.core.management.base import BaseCommand
from wallet_app.utils.webscrapping_indices import get_IPCA, get_dolar_and_euro, get_CDI_and_Selic


class Command(BaseCommand):

    def handle(self, *args, **options):
        get_IPCA()
        get_dolar_and_euro()
        get_CDI_and_Selic()