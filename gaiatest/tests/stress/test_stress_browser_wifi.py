# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaStressTest
from gaiatest.mocks.mock_contact import MockContact
import os
import time

# Approximate runtime per 100 iterations: 30 minutes

class TestStressBrowserWifi(GaiaStressTest):

    # Firefox/chrome locators
    _awesome_bar_locator = ("id", "url-input")
    _url_button_locator = ("id", "url-button")
    _throbber_locator = ("id", "throbber")
    _browser_frame_locator = ('css selector', 'iframe[mozbrowser]')
    _close_button_locator = ('css selector', '#cards-view li.card[data-origin*="browser"] .close-card')

    def setUp(self):
        GaiaStressTest.setUp(self)

        # Name of stress test method to be repeated
        self.test_method = self.browser_wifi

        # Want wifi only
        self.data_layer.disable_cell_data()
        self.data_layer.enable_wifi()
        self.data_layer.connect_to_wifi(self.testvars['wifi'])

    def test_stress_browser_wifi(self):
        self.drive()

    def browser_wifi(self, count):
        # Start browser and load page and verify, code taken from test_browser_cell_data.py
        self.app = self.apps.launch('Browser')
        self.wait_for_condition(lambda m: m.execute_script("return window.wrappedJSObject.Browser.hasLoaded;"))

        awesome_bar = self.marionette.find_element(*self._awesome_bar_locator)
        awesome_bar.send_keys('http://mozqa.com/data/firefox/layout/mozilla.html')

        url_button = self.marionette.find_element(*self._url_button_locator)
        self.marionette.tap(url_button)

        # Wait for throbber
        self.wait_for_element_displayed(*self._throbber_locator)

        # Bump up the timeout due to slower cell data speeds
        self.wait_for_condition(lambda m: not self.is_throbber_visible(), timeout=120)

        browser_frame = self.marionette.find_element(
            *self._browser_frame_locator)

        self.marionette.switch_to_frame(browser_frame)

        self.wait_for_element_present('id', 'page-title', 120)
        heading = self.marionette.find_element('id', 'page-title')
        self.assertEqual(heading.text, 'We believe that the internet should be public, open and accessible.')

        # Wait a couple of seconds with page displayed
        time.sleep(2)

        # Close the browser using home button
        self.close_app()

        # Wait a couple of seconds between iterations
        time.sleep(2)

    def is_throbber_visible(self):
        return self.marionette.find_element(*self._throbber_locator).get_attribute('class') == 'loading'
