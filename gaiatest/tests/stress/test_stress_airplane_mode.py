# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaStressTest

import os
import datetime
import time


class TestStressAirplaneMode(GaiaStressTest):

    _utility_tray_locator = ('css selector', '#utility-tray')
    _airplane_mode_button_locator = ('css selector', '#quick-settings-airplane-mode')
    _airplane_mode_enabled_button_locator = ('css selector', '#quick-settings-airplane-mode[data-enabled]')
    _airplane_mode_enabled_status_locator =  ('css selector', '.sb-icon-flight-mode')
    _network_enabled_status_locator = ('css selector', '.sb-icon-signal[data-level="5"]') # OR OTHER SIGNAL LEVELS!!!
    _wifi_enabled_status_locator = ('css selector', '.sb-icon-wifi') # NEED WIFI LEVEL??

    def setUp(self):
        GaiaStressTest.setUp(self)

        # Set name of stress test method to be repeated
        self.test_method = self.airplane_mode
        
        # **** TODO ***** turn on wifi
        
        # **** TODO ****** turn on mobile network

    def test_stress_airplane_mode(self):
        self.drive()

    def airplane_mode(self, count):
        # Verify NOT in airplane mode
        self.wait_for_element_not_displayed(*self._airplane_mode_enabled_status_locator)
        self.wait_for_element_displayed(*self._network_enabled_status_locator)
        self.wait_for_element_displayed(*self._wifi_enabled_status_locator)

        # Open the utility tray
        self.marionette.execute_script("window.wrappedJSObject.UtilityTray.show()")
        self.wait_for_element_displayed(*self._utility_tray_locator)

        # Click airplane mode button to activate
        self.wait_for_element_displayed(*self._airplane_mode_button_locator)
        airplane_mode_button = self.marionette.find_element(*self._airplane_mode_button_locator)
        self.marionette.tap(airplane_mode_button)
        time.sleep(3)

        # Close the utility tray
        self.marionette.execute_script("window.wrappedJSObject.UtilityTray.hide()")
        self.wait_for_element_not_displayed(*self._utility_tray_locator)

        # Verify ARE in airplane mode
        self.wait_for_element_displayed(*self._airplane_mode_enabled_status_locator)
        self.wait_for_element_not_displayed(*self._network_enabled_status_locator)
        self.wait_for_element_not_displayed(*self._wifi_enabled_status_locator)

        # Open the utility tray
        self.marionette.execute_script("window.wrappedJSObject.UtilityTray.show()")
        self.wait_for_element_displayed(*self._utility_tray_locator)

        # Click airplane mode button to deactivate
        self.wait_for_element_displayed(*self._airplane_mode_enabled_button_locator)
        airplane_mode_button = self.marionette.find_element(*self._airplane_mode_enabled_button_locator)
        self.marionette.tap(airplane_mode_button)
        time.sleep(3)

        # Close the utility tray
        self.marionette.execute_script("window.wrappedJSObject.UtilityTray.hide()")
        self.wait_for_element_not_displayed(*self._utility_tray_locator)