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

    def login_and_get_token(self, email, password, ius_session, thx_guid):
        super().login_and_get_token(email, password, ius_session, thx_guid)

        doc = html.document_fromstring(
            self.get(MINT_OVERVIEW_URL).text)
        self.mint_user_id = json.loads(doc.get_element_by_id('javascript-user').value)['userId']

    def get_session_cookies(self, username, password):
        return_value = super().get_session_cookies(username, password)

        from selenium import webdriver
        driver = webdriver.Chrome()

        driver.get('https://www.mint.com')
        driver.implicitly_wait(20)  # seconds
        driver.find_element_by_link_text('Log In').click()

        driver.find_element_by_id('ius-userid').send_keys(username)
        driver.find_element_by_id('ius-password').send_keys(password)
        driver.find_element_by_id('ius-sign-in-submit-btn').submit()

        while not driver.current_url.startswith(MINT_OVERVIEW_URL):
            time.sleep(1)

        self.browser_auth_api_key = driver.execute_script(
            'return window.MintConfig.browserAuthAPIKey')

        return return_value

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
                   },
                   headers={
                       'authorization':
                           'Intuit_APIKey intuit_apikey={}, intuit_apikey_version=1.0'.format(
                               self.browser_auth_api_key),
                       'content-type': 'application/json'
                   })
