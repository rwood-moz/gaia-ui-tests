# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
from gaiatest import GaiaTestCase
from gaiatest.apps.marketplace.app import Marketplace


class TestSearchMarketplacePaidApp(GaiaTestCase):

    MARKETPLACE_DEV_NAME = 'Marketplace Dev'
    MARKETPLACE_DEV_MANIFEST = 'https://marketplace-dev.allizom.org/manifest.webapp'

    # System app confirmation button to confirm installing an app

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.connect_to_network()
        self.install_marketplace_dev()

    def test_search_paid_app(self):
        marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        marketplace.launch()

        results = marketplace.search('')

        self.assertGreater(len(results.search_results), 0, 'No results found.')

        filter = results.tap_filter()
        filter.by_price('paid')
        results = filter.tap_apply()

        self.assertGreater(len(results.search_results), 0, 'No results found.')

        for result in results.search_results:
            self.assertTrue(re.match('^\$\d+\.\d{2}', result.price),
                            "App %s it's not a paid app." % result.name)

    def install_marketplace_dev(self):
        _yes_button_locator = ('id', 'app-install-install-button')

        if not self.apps.is_app_installed(self.MARKETPLACE_DEV_NAME):
            # install the marketplace dev app
            self.marionette.execute_script('navigator.mozApps.install("%s")' % self.MARKETPLACE_DEV_MANIFEST)

            # TODO add this to the system app object when we have one
            self.wait_for_element_displayed(*_yes_button_locator)
            self.marionette.tap(self.marionette.find_element(*_yes_button_locator))
            self.wait_for_element_not_displayed(*_yes_button_locator)

    def tearDown(self):
        GaiaTestCase.tearDown(self)
