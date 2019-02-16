# mint_bitcoin_sync
A python script that will update Mint.com with current value of cryptos you own. Uses
Blockchain.info API to get price over past 24 hours. Note that there is no public Mint.com API, so this is using
"private" API calls that may break at any point.

# Requirements
* Python 3.x - https://www.python.org/
* ChromeDriver - https://sites.google.com/a/chromium.org/chromedriver/
* `pip install -r requirements`

# Mint.com Setup
1. On Mint.com, a new "account" needs to be added for Bitcoins
2. Click "Add a property"
3. Select "Cash or Debt"
4. Pick "Cash" from dropdown and click "Next" button
5. What would you like to call it? Set it to "Bitcoin" (or call it whatever you want)
6. How much is it worth? Set it to "1" (script will update it to correct value when run)
7. Click 'Add it!' button

# Usage
```
usage: mint_bitcoin_sync.py [-h] -e EMAIL [-p PASSWORD] -l
                            BITCOIN_ACCOUNT_LABEL -c config_file [--version]

Update Mint.com with current value of Bitcoins

optional arguments:
  -h, --help            show this help message and exit
  -e EMAIL              Mint.com Email Address
  -p PASSWORD           Mint.com Password (will prompt if not provided)
  -l BITCOIN_ACCOUNT_LABEL
                        Mint.com Bitcoin account label
  -c CONFIG_FILE        Configuration file containing coin name and amount.
  --version             show program's version number and exit

Note that the first time you use this, you might be prompted by Mint.com to enter a verification code sent to your email.  This should only happen once.
```

# Config File Example:
Coin names must match `id` from https://api.coinmarketcap.com/v1/ticker/
```json
{
"bitcoin": 1.11,
"ethereum": 1.23,
"bitcoin-cash": 0.1234,
"bitcoin-sv": 3.21
}
```


# Example
```
python mint_bitcoin_sync.py -e mintlogin@gmail.com -l Bitcoin -c config.json
Mint.com password:
```
