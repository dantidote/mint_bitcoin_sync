import json
import time

import mintapi
from lxml import html

MINT_OVERVIEW_URL = 'https://mint.intuit.com/overview.event'
PROPERTY_ACCOUNT_URL_FORMAT = \
    'https://mint.intuit.com/mas/v1/providers/PFM:{}_{}/accounts/PFM:OtherPropertyAccount:{}_{}'


class Mint(mintapi.Mint):
    browser_auth_api_key = None
    mint_user_id = None

    def patch(self, url, **kwargs):
      return self.driver.request('PATCH', url, **kwargs)

    def get_userID(self):
        value_json = self.driver.find_element_by_name(
        'javascript-user').get_attribute('value')
        return json.loads(value_json)['userId']

    def get_api_key(self):
        return self.driver.execute_script('return window.MintConfig.browserAuthAPIKey')

    def set_property_account_value(self, account, value):
        account_id = account['accountId']
        account_login_id = account['fiLoginId']
        account_update_url = PROPERTY_ACCOUNT_URL_FORMAT.format(
            self.mint_user_id, account_login_id, self.mint_user_id, account_id)

        self.patch(account_update_url,
                   json={
                       'name': account['accountName'],
                       'value': value,
                       'type': 'OtherPropertyAccount'
                   }
                   ,
                   headers={
                       'authorization':
                           'Intuit_APIKey intuit_apikey={}, intuit_apikey_version=1.0'.format(
                               self.browser_auth_api_key),
                       'content-type': 'application/json'
                   }
                   )
