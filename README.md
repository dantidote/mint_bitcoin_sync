# mint_bitcoin_sync
A python script that will update Mint.com with current value of Bitcoins in specified bitcoin addresses. Uses
Blockchain.info API to get price over past 24 hours. Note that there is no public Mint.com API, so this is using
"private" API calls that may break at any point.

# Requirements
* Python 3.x - https://www.python.org/
* ChromeDriver - https://sites.google.com/a/chromium.org/chromedriver/
<pre>
pip install -r requirements
</pre>

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
                            BITCOIN_ACCOUNT_LABEL [-a BITCOIN_ADDRESSES or XPUBs]
                            [-f BITCOIN_ADDRESS_FILE] [--version]

Update Mint.com with current value of Bitcoins in specified bitcoin addresses or xpub public key

optional arguments:
  -h, --help            show this help message and exit
  -e EMAIL              Mint.com Email Address
  -p PASSWORD           Mint.com Password (will prompt if not provided)
  -l BITCOIN_ACCOUNT_LABEL
                        Mint.com Bitcoin account label
  -a BITCOIN_ADDRESSES  Bitcoin public address or xpub public keys (specify multiple -a for more
                        than one)
  -f BITCOIN_ADDRESS_FILE
                        File containing Bitcoin public addresses or xpub public keys, one
                        address per line. Must specify either -a or -f 
                        argument, must not specify both.
  --version             show program's version number and exit
  
Note that the first time you use this, you might be prompted by Mint.com to enter a verification code sent to your email.  This should only happen once.

```
# Example
```
python mint_bitcoin_sync.py -e mintlogin@gmail.com -l Bitcoin -a xpubxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Mint.com password: 
2017-12-10 19:04:36,851 INFO   line 29   Getting current bitcoin balance from https://blockchain.info/address/xpubxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx?format=json
2017-12-10 19:04:37,352 INFO   line 45   Bitcoin address "xpubxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" has x.xxxxxxxx BTC
2017-12-10 19:04:37,353 INFO   line 9    Getting current bitcoin price from http://blockchain.info/q/24hrprice
2017-12-10 19:04:37,392 INFO   line 23   Using retrieved BTC price: $xxxx.xx
2017-12-10 19:04:37,393 INFO   line 59   Current combined balance for all addresses: $x,xxx.xx

2017-12-10 19:05:25,497 INFO   line 71   Finished
```
