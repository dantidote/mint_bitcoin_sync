import json
import logging
from lxml import html
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

def get_current_price_usd(coin,apikey):
    price_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    logging.info('Getting current %s price from %s', coin, price_url)

    parameters = {
      'convert':'USD',
      'symbol': coin
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': apikey
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
      response = session.get(price_url, params=parameters)
      data = json.loads(response.text)
      return  data["data"][coin.upper()]["quote"]["USD"]["price"]
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print (e)

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
