import argparse
import getpass
import locale
import logging
import json

from lib.blockchaininfo import get_current_price_usd,  get_current_address_balance
from lib.mint import Mint


def main():

    try:
        import keyring
    except ImportError:
        keyring = None

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
    parser.add_argument('-k', action='store', dest='apikey',
                        help='coinmarketcap api key', required=True)
    parser.add_argument(
        '-c', action='store', dest='config_file',
        help='config file')
    parser.add_argument('--keyring', action='store_true', dest='keyring',
      help='Use OS keyring for storing password information')

    parser.add_argument('--version', action='version', version='%(prog)s 1.4')

    args = parser.parse_args()

    if args.keyring and not keyring:
        cmdline.error('--keyring can only be used if the `keyring` '
            'library is installed.')

    # Setup logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-6s line %(lineno)-4s %(message)s')

    if keyring and not args.password:
        # If the keyring module is installed and we don't yet have
        # a password, try prompting for it
        args.password = keyring.get_password('mintapi', args.email)

    # Get password if not provided
    if not args.password:
        args.password = getpass.getpass('Mint.com password: ')

    if args.keyring:
        # If keyring option is specified, save the password in the keyring
        keyring.set_password('mintapi', args.email, args.password)


    with open(args.config_file) as f:
        config = json.load(f)

    total_usd=0
    for k,v in config.items():
      current_price = float(get_current_price_usd(k,args.apikey))
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
