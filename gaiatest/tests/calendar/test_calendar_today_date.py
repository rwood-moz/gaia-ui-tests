# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
import calendar
import time

from gaiatest import GaiaTestCase


DAYS_OF_WEEK = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY',
                'SATURDAY', 'SUNDAY']


class TestCalendar(GaiaTestCase):

    _current_month_year_locator = ('id', 'current-month-year')
    _selected_day_title_locator = ('id', 'selected-day-title')

    def setUp(self):
        GaiaTestCase.setUp(self)

        if self.device.is_android_build:
            # Setting the system time to a hardcoded datetime to avoid timezone issues
            # Jan. 1, 2013, according to http://www.epochconverter.com/
            _seconds_since_epoch = 1357043430
            self.today = datetime.date.fromtimestamp(_seconds_since_epoch)

            # set the system date to an expected date, and timezone to UTC
            self.data_layer.set_time(_seconds_since_epoch * 1000)
            self.data_layer.set_setting('time.timezone', 'Atlantic/Reykjavik')
        else:
            self.today = datetime.date.today()

        # launch the Calendar app
        self.app = self.apps.launch('calendar')

    def test_check_today_date(self):
        # https://moztrap.mozilla.org/manage/case/3751/

        # wait for the selected day and month title to render
        self.wait_for_element_displayed(
            *self._current_month_year_locator)
        self.wait_for_element_displayed(
            *self._selected_day_title_locator)

        # find the default selected day and month title
        selected_day = self.marionette.find_element(
            *self._selected_day_title_locator)
        month_title = self.marionette.find_element(
            *self._current_month_year_locator)

        # validate month title and selected day aligns with today's date
        self.assertEquals(month_title.text, self.today.strftime('%B %Y'))
        self.assertEquals(selected_day.text, self.today.strftime('%A %-d %B %Y').upper())
