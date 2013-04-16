# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
import time


class TestMarketplaceLogin(GaiaTestCase):

    # Marketplace iframe
    _marketplace_iframe_locator = ('css selector', "iframe[src*='marketplace']")

    # Marketplace locators
    _settings_button_locator = ('css selector', 'a.header-button.settings')
    _sign_in_button_locator = ('css selector', 'a.button.browserid')
    _signed_in_notification_locator = ('id', 'notification')
    _sign_out_button_locator = ('css selector', 'a.button.logout')

    _email_account_field_locator = ('id', 'email')

    def setUp(self):
        GaiaTestCase.setUp(self)

        if self.wifi:
            self.data_layer.enable_wifi()
            self.data_layer.connect_to_wifi(self.testvars['wifi'])

        # Launch the app
        self.app = self.apps.launch('Marketplace')

        # Switch to marketplace iframe
        self.marionette.switch_to_frame(self.marionette.find_element(*self._marketplace_iframe_locator))

    def test_login_marketplace(self):
        # https://moztrap.mozilla.org/manage/case/4134/

        self.wait_for_element_displayed(*self._settings_button_locator)
        self.marionette.tap(self.marionette.find_element(*self._settings_button_locator))

        self.wait_for_element_displayed(*self._sign_in_button_locator)
        sign_in_button = self.marionette.find_element(*self._sign_in_button_locator)
        # TODO: click works but not tap
        sign_in_button.click()

        # TODO: This shouldn't be necessary as we are issuing the same command in
        #       _login_to_persona, but some testers have seen improved reliability with it
        self.marionette.switch_to_frame()

        self._login_to_persona(self.testvars['marketplace']['username'],
                               self.testvars['marketplace']['password'])

        # switch back to Marketplace
        self.marionette.switch_to_frame()
        self.marionette.switch_to_frame(self.app.frame)

        # tap on the signed-in notification at the bottom of the screen to dismiss it
        self.wait_for_element_displayed(*self._signed_in_notification_locator)
        self.marionette.tap(self.marionette.find_element(*self._signed_in_notification_locator))

        self.wait_for_element_displayed(*self._sign_out_button_locator)

        # Verify that user is logged in
        self.assertEqual(self.testvars['marketplace']['username'],
                         self.marionette.find_element(*self._email_account_field_locator).get_attribute('value'))

        # Sign out, which should return to the Marketplace home screen
        sign_out_button = self.marionette.find_element(*self._sign_out_button_locator)
        # TODO: click works but not tap
        sign_out_button.click()
        # Without this next line I was getting a StaleElementException
        self.wait_for_element_not_displayed(*self._sign_out_button_locator)

        # Verify that user is signed out
        self.wait_for_element_displayed(*self._settings_button_locator)
        self.marionette.tap(self.marionette.find_element(*self._settings_button_locator))
        self.wait_for_element_displayed(*self._sign_in_button_locator)

    def _login_to_persona(self, username, password):

        _persona_frame_locator = ('css selector', "iframe")

        # Trusty UI on home screen
        _tui_container_locator = ('id', 'trustedui-frame-container')

        # Persona dialog
        _waiting_locator = ('css selector', 'body.waiting')
        _email_input_locator = ('id', 'authentication_email')
        _password_input_locator = ('id', 'authentication_password')
        _next_button_locator = ('css selector', 'button.start')
        _returning_button_locator = ('css selector', 'button.returning')
        _sign_in_button_locator = ('id', 'signInButton')
        _this_session_only_button_locator = ('id', 'this_is_not_my_computer')

        # Switch to top level frame then Persona frame
        self.marionette.switch_to_frame()
        self.wait_for_element_present(*_tui_container_locator)
        trustyUI = self.marionette.find_element(*_tui_container_locator)
        self.wait_for_condition(lambda m: trustyUI.find_element(*_persona_frame_locator))
        personaDialog = trustyUI.find_element(*_persona_frame_locator)
        self.marionette.switch_to_frame(personaDialog)

        # Wait for the loading to complete
        self.wait_for_element_not_present(*_waiting_locator)

        if self.marionette.find_element(*_email_input_locator).is_displayed():
            # Persona has no memory of your details ie after device flash
            email_field = self.marionette.find_element(*_email_input_locator)
            email_field.send_keys(username)

            self.marionette.tap(self.marionette.find_element(*_next_button_locator))

            self.wait_for_element_displayed(*_password_input_locator)
            password_field = self.marionette.find_element(*_password_input_locator)
            password_field.send_keys(password)

            self.wait_for_element_displayed(*_returning_button_locator)
            self.marionette.tap(self.marionette.find_element(*_returning_button_locator))

        else:
            # Persona remembers your username and password
            self.marionette.tap(self.marionette.find_element(*_sign_in_button_locator))

            # Sometimes it prompts for "Remember Me?"
            # If it does, tell it to remember you for this session only
            # TODO: Find out actual logic behind when it prompts or not
            try:
                # We need to wait if the prompt is going to appear, but if it doesn't we don't want to fail the test
                time.sleep(3)

                # TODO: Click works, tap does not
                self.marionette.find_element(*_this_session_only_button_locator).click()
            except:
                pass
