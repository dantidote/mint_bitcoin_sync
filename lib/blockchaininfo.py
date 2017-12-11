import json
import logging
from lxml import html
import requests


def get_bitcoin_current_price_usd():
    price_url = 'http://blockchain.info/q/24hrprice'
    logging.info('Getting current bitcoin price from %s', price_url)

    price_request = requests.get(price_url)
    if price_request.status_code != 200:
        raise Exception(
            'Failed to get price from URL "{}". Error: {}'.format(price_url, price_request.text))
    if not price_request.text:
        raise Exception('No price could be retrieved from URL "{}"'.format(price_url))

    try:
        current_price = float(price_request.text)
    except:
        raise Exception('Failed to convert price "{}" to float'.format(price_request.text))

    logging.info('Using retrieved BTC price: ${:.2f}'.format(current_price))
    return current_price


def get_current_address_balance(public_address):
    balance_url = 'https://blockchain.info/address/{}?format=json'.format(public_address)
    logging.info('Getting current bitcoin balance from %s', balance_url)

    balance_request = requests.get(balance_url)
    if balance_request.status_code != 200 or not balance_request.text:
        raise Exception(
            'Failed to get balance from URL "%s". Error: %s', balance_url, balance_request.text)

    try:
        balance = balance_request.json()['final_balance'] / 100000000.00000000
    except json.JSONDecodeError:
        doc = html.document_fromstring(balance_request.text)
        balance = float(
            doc.get_element_by_id('final_balance').text_content().replace('BTC', '').strip())
    except:
        raise Exception('No balance could be retrieved from URL "%s"', balance_url)

    logging.info('Bitcoin address "%s" has %.8f BTC', public_address, balance)
    return balance
