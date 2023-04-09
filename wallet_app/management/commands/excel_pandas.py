from django.core.management.base import BaseCommand
from wallet_app.utils.excel_database import cc_to_database, reserva_to_database, variable_to_database, \
    fixed_to_database, upload_excel, create_networth_control


class Command(BaseCommand):

    def handle(self, *args, **options):
        data = '/usr/src/app/wallet_app/excel/Tabela planilha.xlm'
        cc_to_database(data, 'Nubank')
        reserva_to_database(data, 'Reserva de Emergencia')
        reserva_to_database(data, 'Compras')
        variable_to_database(data, 'Fundos Imobiliarios')
        fixed_to_database(data, 'Renda Fixa')
        upload_excel(data)
        create_networth_control()
