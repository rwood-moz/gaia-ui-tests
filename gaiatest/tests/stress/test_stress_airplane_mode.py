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

    # Cell data strength signal status icons
    _network_enabled_negative_locator = ('css selector', '.sb-icon-signal[data-level="-1"]')
    _network_enabled_level0_locator = ('css selector', '.sb-icon-signal[data-level="0"]')
    _network_enabled_level1_locator = ('css selector', '.sb-icon-signal[data-level="1"]')
    _network_enabled_level2_locator = ('css selector', '.sb-icon-signal[data-level="2"]')
    _network_enabled_level3_locator = ('css selector', '.sb-icon-signal[data-level="3"]')
    _network_enabled_level4_locator = ('css selector', '.sb-icon-signal[data-level="4"]')
    _network_enabled_level5_locator = ('css selector', '.sb-icon-signal[data-level="5"]')
    _network_enabled_searching_locator = ('css selector', 'sb-icon-signal[data-level="-1"][data-searching="true"]')

    # Wifi status icons
    _wifi_enabled_connecting_locator = ('css selector', '.sb-icon-wifi[data-level="0"][data-connecting="true"]')
    _wifi_enabled_level0_locator = ('css selector', '.sb-icon-wifi[data-level="0"]')
    _wifi_enabled_level1_locator = ('css selector', '.sb-icon-wifi[data-level="1"]')
    _wifi_enabled_level2_locator = ('css selector', '.sb-icon-wifi[data-level="2"]')
    _wifi_enabled_level3_locator = ('css selector', '.sb-icon-wifi[data-level="3"]')
    _wifi_enabled_level4_locator = ('css selector', '.sb-icon-wifi[data-level="4"]')

    _network_signal_icon_list = [_network_enabled_negative_locator, 
                                 _network_enabled_level0_locator,
                                 _network_enabled_level1_locator,
                                 _network_enabled_level2_locator,
                                 _network_enabled_level3_locator,
                                 _network_enabled_level4_locator,
                                 _network_enabled_level5_locator,
                                 _network_enabled_searching_locator]

    _wifi_signal_icon_list = [_wifi_enabled_connecting_locator,
                              _wifi_enabled_level0_locator,
                              _wifi_enabled_level1_locator,
                              _wifi_enabled_level2_locator,
                              _wifi_enabled_level3_locator,
                              _wifi_enabled_level4_locator]

    def setUp(self):
        GaiaStressTest.setUp(self)

        # Set name of stress test method to be repeated
        self.test_method = self.airplane_mode

        # Connect wifi
        self.data_layer.enable_wifi()
        self.data_layer.connect_to_wifi(self.testvars['wifi'])

    def test_stress_airplane_mode(self):
        self.drive()

    def airplane_mode(self, count):
        # Must look for lots of icons so set find timeout to 1/2 a second
        self.marionette.set_search_timeout(1000)

        # Verify NOT in airplane mode
        self.wait_for_element_not_displayed(*self._airplane_mode_enabled_status_locator)
        self.wait_for_condition(self.verify_cell_signal_present, 1, "Cell network signal icon not found")
        self.wait_for_condition(self.verify_wifi_signal_present, 1, "Wifi signal icon not found")

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
        self.wait_for_condition(self.verify_cell_signal_absent, 1, "Cell network signal icon displayed but shouldn't be")
        self.wait_for_condition(self.verify_wifi_signal_absent, 1, "Wifi signal icon displayed but shouldn't be")

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

    def verify_cell_signal_present(self, x):
        # Verify the network cell signal icon is displayed; can be various signal strengths
        for net_icon in self._network_signal_icon_list:
            if self.is_element_present(*net_icon):
                if self.marionette.find_element(*net_icon).is_displayed():
                    return True
        return False

    def verify_cell_signal_absent(self, x):
        # Verify cell signal status icon is not displayed; can be various network strengths
        for net_icon in self._network_signal_icon_list:
            if self.is_element_present(*net_icon):
                if self.marionette.find_element(*net_icon).is_displayed():
                    return False
        return True

    def verify_wifi_signal_present(self, x):
        # Verify the network cell signal icon is displayed; can be various signal strengths
        for wifi_icon in self._wifi_signal_icon_list:
            if self.is_element_present(*wifi_icon):
                if self.marionette.find_element(*wifi_icon).is_displayed():
                    return True
        return False

    def verify_wifi_signal_absent(self, x):
        # Verify cell signal status icon is not displayed; can be various network strengths
        for wifi_icon in self._wifi_signal_icon_list:
            if self.is_element_present(*wifi_icon):
                if self.marionette.find_element(*wifi_icon).is_displayed():
                    return False
        return True
