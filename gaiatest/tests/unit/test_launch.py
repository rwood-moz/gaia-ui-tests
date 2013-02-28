# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestLaunch(GaiaTestCase):

    def test_cold_launch(self):
        app = self.apps.launch('Clock')
        self.assertTrue(app.frame)
        self.assertTrue('clock' in self.marionette.get_url())

    def test_warm_launch(self):
        cold = self.apps.launch('Clock')
        self.apps.launch('Calendar')
        warm = self.apps.launch('Clock')
        self.assertEqual(cold, warm)
        self.assertTrue('clock' in self.marionette.get_url())

    def test_launch_twice(self):
        cold = self.apps.launch('Clock')
        warm = self.apps.launch('Clock')
        self.assertEqual(cold, warm)
        self.assertTrue('clock' in self.marionette.get_url())
