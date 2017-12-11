import argparse
import getpass
import locale
import logging

from lib.blockchaininfo import get_bitcoin_current_price_usd, get_current_address_balance
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
    parser.add_argument('-a', action='append', default=[], dest='bitcoin_addresses',
                        help='Bitcoin public address/xpub (specify multiple -a for more than one)')
    parser.add_argument(
        '-f', action='store', dest='bitcoin_address_file',
        help='Bitcoin public address/xpub file containing one address/xpub per line')

    parser.add_argument('--version', action='version', version='%(prog)s 1.4')

    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-6s line %(lineno)-4s %(message)s')

    # Get password if not provided
    if not args.password:
        args.password = getpass.getpass('Mint.com password: ')

    # Get addresses from file if not provided by -a argument
    if not args.bitcoin_addresses:
        if not args.bitcoin_address_file:
            print('must provide either -a or -f argument')
            return
        file = open(args.bitcoin_address_file, 'r')
        args.bitcoin_addresses = file.read().splitlines()
        file.close()

    # Get bitcoin balance and price
    bitcoin_balance = 0.00000000
    for address in args.bitcoin_addresses:
        bitcoin_balance += get_current_address_balance(address)
    current_bitcoin_price_usd = get_bitcoin_current_price_usd()

    # Determine current balance
    total_usd = bitcoin_balance * current_bitcoin_price_usd
    locale.setlocale(locale.LC_ALL, '')
    total_usd_string = locale.currency(total_usd, grouping=True)
    logging.info('Current combined balance for all addresses: %s\n', total_usd_string)

    # Initialize mint object
    mint = Mint(args.email, args.password)

    # Get all accounts
    mint_accounts = mint.get_accounts()
    bitcoin_account = [
        account for account in mint_accounts if account['accountName'] == args.bitcoin_account_label
    ][0]
    mint.set_property_account_value(bitcoin_account, total_usd)

    logging.info('Finished')


if __name__ == '__main__':
    main()
