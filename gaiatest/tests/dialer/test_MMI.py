# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from gaiatest import GaiaTestCase

IMEI_CODE = "*#06#"
CALL_FORWARDING_CODE = "*#21#"

class TestMMI(GaiaTestCase):

    # Dialer app
    _keyboard_container_locator = ('id', 'keyboard-container')
    _phone_number_view_locator = ('id', 'phone-number-view')
    _call_bar_locator = ('id', 'keypad-callbar-call-action')

    # Attention frame
    _attention_frame_locator = ('xpath', '//*[@id="attention-screen"]/iframe')
    _message_locator = ('id', 'message')

    def setUp(self):
        GaiaTestCase.setUp(self)

        # launch the app
        self.app = self.apps.launch('Phone')

    def test_MMI_code_IMEI(self):
        self.wait_for_element_displayed(*self._keyboard_container_locator)

        self._dial_number(IMEI_CODE)

        # Assert that the number was entered correctly.
        phone_view = self.marionette.find_element(*self._phone_number_view_locator)
        self.assertEqual(phone_view.get_attribute('value'), IMEI_CODE)

        # Click the call button
        self.marionette.tap(self.marionette.find_element(*self._call_bar_locator))

        self.marionette.switch_to_frame()

        self.wait_for_element_displayed(*self._attention_frame_locator)
        attention_frame = self.marionette.find_element(*self._attention_frame_locator)

        # Switch to attention frame
        self.marionette.switch_to_frame(attention_frame)

        imei = self.marionette.find_element(*self._message_locator).text

        self.assertEqual(imei, self.testvars['imei'])

    def _dial_number(self, phone_number):
        '''
        Dial a number using the keypad
        '''

        for i in phone_number:
            if i == "+":
                zero_button = self.marionette.find_element('css selector', 'div.keypad-key[data-value="0"]')
                self.marionette.long_press(zero_button, 1200)
                # Wait same time as the long_press to bust the asynchronous
                # TODO https://bugzilla.mozilla.org/show_bug.cgi?id=815115
                time.sleep(2)

            else:
                self.marionette.tap(self.marionette.find_element('css selector', 'div.keypad-key[data-value="%s"]' % i))
                time.sleep(0.25)
