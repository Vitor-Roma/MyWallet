from _decimal import Decimal
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from wallet_app.models import Indexes
from wallet_app.utils.global_functions import round_percent_string_to_decimal


def get_IPCA(driver):
    driver.get('https://www.ibge.gov.br/explica/inflacao.php')
    IPCA = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'variavel-dado')))[
        1].text
    index = Indexes.objects.get(name='IPCA')
    index.value = round_percent_string_to_decimal(IPCA)
    index.is_percent = True
    try:
        index.save()
    except:
        print(f'Erro ao atualizar o valor do índice: {index.name}')


def get_dolar_and_euro(driver):
    driver.get(
        'https://www.google.com/search?q=pre%C3%A7o+dolar&client=ubuntu&hs=38r&channel=fs&sxsrf=AJOqlzW-FJY1skru4GBwk2B4ziCsO-ILXw%3A1673413784418&ei=mES-Y_GaGfHM1sQPsfqn4A0&ved=0ahUKEwjxxrqR4L78AhVxppUCHTH9CdwQ4dUDCA4&uact=5&oq=pre%C3%A7o+dolar&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzILCAAQgAQQsQMQgwEyCwgAEIAEELEDEIMBMgsIABCABBCxAxCDATIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6CggAEEcQ1gQQsAM6BAgjECc6BggjECcQEzoLCC4QgAQQsQMQgwE6CAgAELEDEIMBOgQIABBDOg4IABCABBCxAxCDARDJAzoKCC4QsQMQgwEQQzoICC4QsQMQgwE6CAgAEIAEELEDOhAIABCABBCxAxCDARBGEIICSgQIQRgASgQIRhgAULYGWOgOYLMPaANwAXgAgAGGAYgBgQmSAQMxLjmYAQCgAQHIAQjAAQE&sclient=gws-wiz-serp')
    div = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'knowledge-currency__updatable-data-column')))
    dolar = WebDriverWait(div, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'span')))[2].text
    index = Indexes.objects.get(name='Dolar')
    index.value = Decimal(dolar.replace(',', '.'))
    try:
        index.save()
    except:
        print(f'Erro ao atualizar o valor do índice: {index.name}')
    driver.get(
        'https://www.google.com/search?q=pre%C3%A7o+euro&client=ubuntu&channel=fs&sxsrf=AJOqlzWBvYUiKS0jGSyH9NNS3P9UGpGH0Q%3A1673416187273&ei=-02-Y8ClEIH71sQP-_SCoAU&ved=0ahUKEwiAj52L6b78AhWBvZUCHXu6AFQQ4dUDCA4&uact=5&oq=pre%C3%A7o+euro&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIQCAAQgAQQsQMQgwEQRhCCAjIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDoKCAAQRxDWBBCwAzoNCAAQRxDWBBDJAxCwAzoICAAQkgMQsAM6BAgjECc6CwgAEIAEELEDEIMBOgkIIxAnEEYQggI6CAgAEIAEELEDOggIABCxAxCDAToKCAAQsQMQgwEQQzoECAAQQzoOCAAQgAQQsQMQgwEQyQNKBAhBGABKBAhGGABQ4g5Ygx1g3R5oAnABeACAAZ4BiAGwCJIBAzAuOZgBAKABAcgBCsABAQ&sclient=gws-wiz-serp')
    div = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'knowledge-currency__updatable-data-column')))
    euro = WebDriverWait(div, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'span')))[2].text
    index = Indexes.objects.get(name='Euro')
    index.value = Decimal(euro.replace(',', '.'))
    try:
        index.save()
    except:
        print(f'Erro ao atualizar o valor do índice: {index.name}')


def get_CDI_and_Selic(driver):
    driver.get('https://www.mobills.com.br/blog/investimentos/tudo-sobre-cdi/')
    table = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
    tr = WebDriverWait(table, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))[1]
    td = WebDriverWait(tr, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'td')))[1].text
    CDI = td.split('%')[0].replace(',', '.')
    index = Indexes.objects.get(name='CDI')
    index.value = CDI
    index.is_percent = True
    try:
        index.save()
    except:
        print(f'Erro ao atualizar o valor do índice: {index.name}')
    index = Indexes.objects.get(name='Selic')
    index.value = CDI
    index.is_percent = True
    try:
        index.save()
    except:
        print(f'Erro ao atualizar o valor do índice: {index.name}')


def get_BITCOIN_and_ETHEREUM(driver):
    driver.get('https://www.binance.com/pt-BR/price/bitcoin')
    usd_bitcoin = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'css-1bwgsh3'))).text[2:].replace(',', '')
    usd_bitcoin = Decimal(usd_bitcoin)
    dollar = Indexes.objects.get(name="Dolar")
    brl_bitcoin = round(usd_bitcoin * dollar.value, 2)
    try:
        index = Indexes.objects.get(name='Bitcoin')
        index.value = brl_bitcoin
        index.save()
    except Indexes.DoesNotExist:
        index = Indexes.objects.create(name='Bitcoin', value=brl_bitcoin)
    except:
        print(f'Erro ao atualizar o valor do índice: {index.name}')

    driver.get('https://www.binance.com/pt-BR/price/ethereum')
    usd_ethereum = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'css-1bwgsh3'))).text[2:].replace(',', '')
    usd_ethereum = Decimal(usd_ethereum)
    dollar = Indexes.objects.get(name="Dolar")
    brl_ethereum = round(usd_ethereum * dollar.value, 2)
    try:
        index = Indexes.objects.get(name='Ethereum')
        index.value = brl_ethereum
        index.save()
    except Indexes.DoesNotExist:
        index = Indexes.objects.create(name='Ethereum', value=brl_ethereum)
    except:
        print(f'Erro ao atualizar o valor do índice: {index.name}')
