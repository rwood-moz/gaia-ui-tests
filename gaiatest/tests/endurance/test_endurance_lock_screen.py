# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Approximate runtime per 100 iterations: xxx minutes

from gaiatest import GaiaEnduranceTest

import os
import datetime
import time


class TestEnduranceLockScreen(GaiaEnduranceTest):

    _lockscreen_locator = ('id', 'lockscreen')
    _statusbar_time_display_locator = ('css selector', '#statusbar-time')

    def setUp(self):
        # Note: Screen is unlocked automatically at start of test
        GaiaEnduranceTest.setUp(self)

        # Set name of endurance test method to be repeated
        self.test_method = self.lock_screen

        # Specify name of gaia app under test (required for DataZilla)
        self.app_under_test = "homescreen"

    def test_endurance_lock_screen(self):
        self.drive()

    def lock_screen(self, count):
        # Verify screen is unlocked
        self.wait_for_element_not_displayed(*self._lockscreen_locator)
        self.wait_for_element_displayed(*self._statusbar_time_display_locator)

        # Lock screen
        self.lockscreen.lock()
        time.sleep(2)

        # verify screen is locked
        self.wait_for_element_displayed(*self._lockscreen_locator)
        self.wait_for_element_not_displayed(*self._statusbar_time_display_locator)

        # Unlock screen
        self.lockscreen.unlock()
        time.sleep(2)
