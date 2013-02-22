# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaStressTest
from gaiatest.tests.clock import clock_object

import os
import datetime
import time


class TestStressSetAlarm(GaiaStressTest):

    # See clock_object.py for element locators etc.

    def setUp(self):
        GaiaStressTest.setUp(self)

        # Set name of stress test method to be repeated
        self.test_method = self.set_alarm

        # Launch the Clock app and verify
        self.app = self.apps.launch('Clock')
        self.wait_for_element_displayed(*clock_object._alarm_create_new_locator)

    def test_stress_add_event(self):
        self.drive()

    def set_alarm(self, count):
        # Set a new alarm and verify; code taken from existing clock tests

        # Get the number of alarms set, before adding the new alarm
        initial_alarms_count = len(self.marionette.find_elements(*clock_object._all_alarms))

        # create a new alarm, default values except label
        alarm_create_new = self.marionette.find_element(*clock_object._alarm_create_new_locator)
        self.marionette.tap(alarm_create_new)
        self.wait_for_element_displayed(*clock_object._new_alarm_label)

        # Set label
        alarm_label = self.marionette.find_element(*clock_object._new_alarm_label)
        alarm_label.clear()
        text = "%d of %d" %(count, self.iterations)
        alarm_label.send_keys(text)

        self.wait_for_element_displayed(*clock_object._alarm_save_locator)
        alarm_save = self.marionette.find_element(*clock_object._alarm_save_locator)
        self.marionette.tap(alarm_save)

        # verify the banner-countdown message appears
        self.wait_for_element_displayed(*clock_object._banner_countdown_notification_locator)
        alarm_msg = self.marionette.find_element(*clock_object._banner_countdown_notification_locator).text
        self.assertTrue('The alarm is set for' in alarm_msg, 'Actual banner message was: "' + alarm_msg + '"')

        # Wait for banner-countdown to disappear
        self.wait_for_element_not_displayed(*clock_object._banner_countdown_notification_locator)

        # Get the number of alarms set after the new alarm was added
        new_alarms_count = len(self.marionette.find_elements(*clock_object._all_alarms))

        # Ensure the new alarm has been added and is displayed
        self.assertTrue(initial_alarms_count < new_alarms_count,
                        'Alarms count did not increment')
