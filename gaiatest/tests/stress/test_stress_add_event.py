# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase

import os
import datetime


class TestStressAddEvent(GaiaTestCase):

    _current_month_year_locator = ('id', 'current-month-year')
    _selected_day_title_locator = ('id', 'selected-day-title')
    _add_event_button_locator = ('xpath', "//a[@href='/add/']")
    _event_title_input_locator = ('xpath', "//input[@data-l10n-id='event-title']")
    _event_location_input_locator = ('xpath', "//input[@data-l10n-id='event-location']")
    _event_start_time_input_locator = ('xpath', "//input[@data-l10n-id='event-start-time']")
    _event_end_time_input_locator = ('xpath', "//input[@data-l10n-id='event-end-time']")
    _save_event_button_locator = ('css selector', 'button.save')
    _event_list_locator = ('id', 'event-list')
    _week_display_button_locator = ('xpath', "//a[@href='/week/']")
    _day_display_button_locator = ('xpath', "//a[@href='/day/']")
    _week_view_locator = ('id', 'week-view')
    _day_view_locator = ('id', 'day-view')
    _delete_event_button_locator = ('css selector', '#modify-event-view button[data-l10n-id=event-delete]')

    def setUp(self):
        GaiaTestCase.setUp(self)

        try:
            self.min_iterations = self.testvars['stresstests']['min_iterations']
        except:
            self.min_iterations = 100

        # Set iterations, ensure at least at minimum
        try:
            self.iterations = self.testvars['stresstests']['add_event_iterations']
            if (self.iterations < self.min_iterations):
                self.iterations = self.min_iterations
        except:
            self.iterations = self.min_iterations

        # Get checkpoint, if not specified just do one at start and end
        try:
            self.checkpoint_every = self.testvars['stresstests']['add_event_checkpoint']
        except:
            # Not specified, so just do at start and end
            self.checkpoint_every = self.iterations

        # Setting the system time to a hardcoded datetime to avoid timezone issues
        # Jan. 1, 2013, according to http://www.epochconverter.com/
        _seconds_since_epoch = 1357043430
        self.today = datetime.datetime.utcfromtimestamp(_seconds_since_epoch)

        # set the system date to an expected date, and timezone to UTC
        self.data_layer.set_time(_seconds_since_epoch * 1000)
        self.data_layer.set_setting('time.timezone', 'Atlantic/Reykjavik')

        # launch the Calendar app
        self.app = self.apps.launch('calendar')

    def test_stress_add_event(self):
        # Starting checkpoint
        self.checkpoint()

        # Actual test case iterations        
        for count in range(1, self.iterations + 1):
            self.marionette.log("Add contact iteration %d of %d" % (count, self.iterations))
            self.add_event(count)
            # Checkpoint time?
            if ((count % self.checkpoint_every) == 0):
                self.checkpoint(count)

    def add_event(self, count):
        event_title = "Event Title %s" % str(time.time())
        event_location = "Event Location %s" % str(time.time())
        event_start_time = "01:00:00"
        event_end_time = "02:00:00"
        formatted_today = self.today.strftime("%b %d")
        this_event_time_slot_locator = (
            'css selector',
            '#event-list section.hour-1 span.display-hour')
        month_view_time_slot_all_events_locator = (
            'css selector',
            '#event-list section.hour-1 div.events')
        week_view_time_slot_all_events_locator = (
            'css selector',
            "#week-view section.active[data-date*='%s'] ol.hour-1" % formatted_today)
        day_view_time_slot_all_events_locator = (
            'css selector',
            "#day-view section.active[data-date*='%s'] section.hour-1" % formatted_today)
        day_view_time_slot_individual_events_locator = (
            'css selector',
            "#day-view section.active[data-date*='%s'] section.hour-1 div.events div.container" % formatted_today)

        # wait for the add event button to appear
        self.wait_for_element_displayed(*self._add_event_button_locator)

        # click the add event button
        add_event_button = self.marionette.find_element(*self._add_event_button_locator)
        self.marionette.tap(add_event_button)
        self.wait_for_element_displayed(*self._event_title_input_locator)

        # create a new event
        self.marionette.find_element(*self._event_title_input_locator).send_keys(event_title)
        self.marionette.find_element(*self._event_location_input_locator).send_keys(event_location)
        self.marionette.find_element(*self._event_start_time_input_locator).clear()
        self.marionette.find_element(*self._event_start_time_input_locator).send_keys(event_start_time)
        self.marionette.find_element(*self._event_end_time_input_locator).clear()
        self.marionette.find_element(*self._event_end_time_input_locator).send_keys(event_end_time)
        save_event_button = self.marionette.find_element(*self._save_event_button_locator)
        self.marionette.tap(save_event_button)

        # wait for the default calendar display
        self.wait_for_element_displayed(*this_event_time_slot_locator)

        # assert that the event is displayed as expected
        self.assertTrue(self.marionette.find_element(*this_event_time_slot_locator).is_displayed(),
                        "Expected the time slot for the event to be present.")
        displayed_events = self.marionette.find_element(*month_view_time_slot_all_events_locator).text
        self.assertIn(event_title, displayed_events)
        self.assertIn(event_location, displayed_events)

        # switch to the week display
        week_display_button = self.marionette.find_element(*self._week_display_button_locator)
        self.marionette.tap(week_display_button)

        self.wait_for_element_displayed(*week_view_time_slot_all_events_locator)
        displayed_events = self.marionette.find_element(*week_view_time_slot_all_events_locator).text
        self.assertIn(event_title, displayed_events)

        # switch to the day display
        day_display_button = self.marionette.find_element(*self._day_display_button_locator)
        self.marionette.tap(day_display_button)

        self.wait_for_element_displayed(*day_view_time_slot_all_events_locator)
        displayed_events = self.marionette.find_element(*day_view_time_slot_all_events_locator).text
        self.assertIn(event_title, displayed_events)
        self.assertIn(event_location, displayed_events)

        # delete all events in the time slot
        all_events = self.marionette.find_elements(*day_view_time_slot_individual_events_locator)
        while len(all_events) > 0:
            self.marionette.tap(all_events[0])
            self.wait_for_element_displayed(*self._event_title_input_locator)
            delete_event_button = self.marionette.find_element(*self._delete_event_button_locator)
            self.marionette.tap(delete_event_button)

            self.wait_for_element_displayed(*self._day_view_locator)
            all_events = self.marionette.find_elements(*day_view_time_slot_individual_events_locator)

    def checkpoint(self, iteration = 0):
        self.marionette.log("Checkpoint")
        if iteration == 0:
            os.system("echo test_stress_add_contacts > checkpoint.log")
        text = "echo checkpoint at iteration %d: >> checkpoint.log" % iteration
        os.system(text)
        os.system("adb shell b2g-ps >> checkpoint.log")
