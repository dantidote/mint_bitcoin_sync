import argparse
import getpass
import locale
import logging
import json

from lib.blockchaininfo import get_current_price_usd,  get_current_address_balance
from lib.mint import Mint


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(
        description='Update Mint.com with current value of Bitcoins in specified bitcoin addresses'
    )

    parser.add_argument('-e', action='store', dest='email',
                        help='Mint.com Email Address', required=True)
    parser.add_argument('-p', action='store', dest='password',
                        help='Mint.com Password (will prompt if not provided)')
    parser.add_argument('-l', action='store', dest='bitcoin_account_label',
                        help='Mint.com Bitcoin account label', required=True)
    parser.add_argument(
        '-c', action='store', dest='config_file',
        help='config file')

    parser.add_argument('--version', action='version', version='%(prog)s 1.4')

    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-6s line %(lineno)-4s %(message)s')

    # Get password if not provided
    if not args.password:
        args.password = getpass.getpass('Mint.com password: ')


    with open(args.config_file) as f:
        config = json.load(f)

    total_usd=0
    for k,v in config.items():
      current_price = float(get_current_price_usd(k))
      amount_usd = current_price * float(v)
      logging.info('%s: %f * %f = %f', k, v, current_price, amount_usd)
      total_usd += amount_usd
      print (total_usd)

    locale.setlocale(locale.LC_ALL, '')
    total_usd_string = locale.currency(total_usd, grouping=True)
    logging.info('Current combined balance for all addresses: %s\n', total_usd_string)

    # Initialize mint object
    mint = Mint(args.email, args.password, headless=True)

    # Get all accounts
    mint_accounts = mint.get_accounts()

    mint.mint_user_id = mint.get_userID()
    mint.browser_auth_api_key = mint.get_api_key()

    bitcoin_account = [
        account for account in mint_accounts if account['accountName'] == args.bitcoin_account_label
    ][0]
    mint.set_property_account_value(bitcoin_account, total_usd)

    logging.info('Finished')


if __name__ == '__main__':
    main()
