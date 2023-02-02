from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from wallet_app.utils.global_functions import round_percent_string_to_decimal


def fiis_value(share_list):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--remote-debugging-port=9222')
    driver = webdriver.Chrome(options=chrome_options)
    for share in share_list:
        page = f'https://www.fundsexplorer.com.br/funds/{share.name}'
        driver.get(page)
        element = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'price')))
        price = element.text[3:]
        try:
            share.current_value = round_percent_string_to_decimal(price)
            share.save()
        except:
            print(f'Erro ao atualizar o valor do fundo: {share.name}')
