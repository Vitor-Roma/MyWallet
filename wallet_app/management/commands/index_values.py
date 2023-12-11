from django.core.management.base import BaseCommand
from wallet_app.utils.webscrapping_indices import *
from wallet_app.utils.get_driver import get_driver


class Command(BaseCommand):

    def handle(self, *args, **options):
        driver = get_driver()

        get_IPCA(driver)
        get_dolar_and_euro(driver)
        get_CDI_and_Selic(driver)
        get_BITCOIN_and_ETHEREUM(driver)
