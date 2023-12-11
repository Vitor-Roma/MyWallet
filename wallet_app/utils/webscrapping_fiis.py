from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from wallet_app.utils.global_functions import round_percent_string_to_decimal


def fiis_value(share_list, driver):
    for share in share_list:
        page = f'https://www.fundsexplorer.com.br/funds/{share.name}'
        driver.get(page)
        element = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'headerTicker__content__price')))
        price = element.text[3:8]
        try:
            share.current_value = round_percent_string_to_decimal(price)
            share.save()
        except:
            print(f'Erro ao atualizar o valor do fundo: {share.name}')
