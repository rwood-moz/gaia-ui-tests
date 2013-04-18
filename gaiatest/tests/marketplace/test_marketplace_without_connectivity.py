# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestMarketplaceWithoutConnectivity(GaiaTestCase):

    # Marketplace iframe
    _marketplace_iframe_locator = ('css selector', "iframe[src*='marketplace']")

    _error_title_locator = ('css selector', '#appError-appframe1 h3[data-l10n-id="error-title"]')
    _error_message_locator = ('css selector', '#appError-appframe1 span[data-l10n-id="error-message"]')
    _expected_error_title = u'Network connection unavailable'
    _expected_error_message = u'Marketplace requires a network connection. Try connecting to a Wi-Fi or mobile data network.'

    def test_marketplace_without_connectivity(self):
        self.app = self.apps.launch('Marketplace')
        self.marionette.switch_to_frame(self.marionette.find_element(*self._marketplace_iframe_locator))
        self.marionette.switch_to_frame()

        self.wait_for_element_displayed(*self._error_title_locator)
        title = self.marionette.find_element(*self._error_title_locator)
        message = self.marionette.find_element(*self._error_message_locator)

        self.assertEqual(title.text, self._expected_error_title)
        self.assertEqual(message.text, self._expected_error_message)
