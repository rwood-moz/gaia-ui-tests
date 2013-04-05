# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestCostControlFTU(GaiaTestCase):

    # 1st step screen locators
    _welcome_title_locator = ('css selector', 'h1[data-l10n-id="fte-welcome-title"]')
    _next_button_locator_1 = ('css selector', '#step-1 span[data-l10n-id="next"]')

    # 2nd step screen locators
    _data_report_title_locator = ('css selector', 'h1[data-l10n-id="fte-onlydata2-title"]')
    _rest_report_period_select_locator = ('css selector', '#non-vivo-step-1 select')
    _next_button_locator_2 = ('css selector', '#non-vivo-step-1 span[data-l10n-id="next"]')

    # 3rd step screen locators
    _data_alert_title_locator = ('css selector', '#non-vivo-step-2 h1[data-l10n-id="fte-onlydata3-title"]')
    _ftu_usage_locator = ('css selector', '#non-vivo-step-2 span.tag')
    _ftu_data_alert_switch_locator = ('css selector', '#non-vivo-step-2 label.end input')
    _ftu_data_alert_label_locator = ('css selector', '#non-vivo-step-2 label.end')
    _capacity_button_locator = ('css selector', '#data-limit-dialog form button')
    _size_input_locator = ('css selector', '#data-limit-dialog form input')
    _usage_done_button_locator = ('id', 'data-usage-done-button')
    _go_button_locator = ('css selector', '#non-vivo-step-2 button.recommend')

    _usage_app_title_locator = ('css selector', 'h1[data-l10n-id="usage"]')

    def setUp(self):
        GaiaTestCase.setUp(self)

        # launch the Usage app
        self.app = self.apps.launch('Usage')

    def test_cost_control_ftu(self):

        # if ftu shows up, continue to do what we should do. Otherwise, trigger it from javascript.
        try:
            self.wait_for_element_displayed(*self._welcome_title_locator)
        except:
            # this is to make fte of usage app came out
            self.marionette.execute_script("return window.wrappedJSObject.ConfigManager.setOption({ fte: true });")
            self.marionette.refresh()

        # wait for welcome screen again and click 'next' to exit welcome screen
        self.wait_for_element_displayed(*self._welcome_title_locator)
        next = self.marionette.find_element(*self._next_button_locator_1)
        self.marionette.tap(next)

        # change the reset report to weekly
        self.wait_for_element_displayed(*self._data_report_title_locator)
        reset_time = self.marionette.find_element(*self._rest_report_period_select_locator)
        # tap() not working here, switch to use click() - see bug #850819
        reset_time.click()
        self._select('Weekly')

        # click 'next'
        next = self.marionette.find_element(*self._next_button_locator_2)
        self.marionette.tap(next)

        # enable the switch for data alert
        self.wait_for_element_displayed(*self._data_alert_title_locator)
        switch = self.marionette.find_element(*self._ftu_data_alert_switch_locator)
        if not switch.is_selected():
            label = self.marionette.find_element(*self._ftu_data_alert_label_locator)
            self.marionette.tap(label)

        # change the data alert from whatever the setting is to 0.1MB
        self.wait_for_element_displayed(*self._ftu_usage_locator)
        usage = self.marionette.find_element(*self._ftu_usage_locator)
        self.marionette.tap(usage)
        # try to get what's the capacity now
        capacity = self.marionette.find_element(*self._capacity_button_locator)
        # there are two choice in this switch u'GB' or u'MB'. if it is u'GB', try to switch to u'MB'
        if capacity.text == u'GB':
            self.marionette.tap(capacity)
        # make sure it is u'MB'
        self.assertEqual(capacity.text, u'MB')

        # clear the original assigned value and set it to 0.1
        size = self.marionette.find_element(*self._size_input_locator)
        size.clear()
        size.send_keys('0.1')
        done = self.marionette.find_element(*self._usage_done_button_locator)
        self.marionette.tap(done)

        self.wait_for_element_displayed(*self._data_alert_title_locator)
        go = self.marionette.find_element(*self._go_button_locator)
        self.marionette.tap(go)

        self.wait_for_element_displayed(*self._usage_app_title_locator)

    # temporarily solution for select options
    def _select(self, match_string):
        # cheeky Select wrapper until Marionette has its own
        # due to the way B2G wraps the app's select box we match on text

        # have to go back to top level to get the B2G select box wrapper
        self.marionette.switch_to_frame()

        options = self.marionette.find_elements('css selector', '#value-selector-container li')
        close_button = self.marionette.find_element('css selector', 'button.value-option-confirm')

        # loop options until we find the match
        for li in options:
            if li.text == match_string:
                li.click()
                break

        close_button.click()

        # now back to app
        self.marionette.switch_to_frame(self.app.frame)
