# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from gaiatest import GaiaTestCase
from gaiatest.apps.browser.app import Browser


class TestCostControlDataAlertMobile(GaiaTestCase):

    # fte locators (can be removed once javascript starts to work)
    _welcome_title_locator = ('css selector', 'h1[data-l10n-id="fte-welcome-title"]')
    _next_button_locator_1 = ('css selector', '#step-1 span[data-l10n-id="next"]')
    _data_report_title_locator = ('css selector', 'h1[data-l10n-id="fte-onlydata2-title"]')
    _next_button_locator_2 = ('css selector', '#non-vivo-step-1 span[data-l10n-id="next"]')
    _data_alert_title_locator = ('css selector', 'section#non-vivo-step-2 h1[data-l10n-id="fte-onlydata3-title"]')
    _go_button_locator = ('css selector', '#non-vivo-step-2 button.recommend')

    # usage main screen locators
    _usage_app_main_locator = ('id', 'datausage-tab')
    _usage_app_title_locator = ('css selector', 'h1[data-l10n-id="usage"]')

    # main screen switch locators
    _mobile_data_item_locator = ('id', 'mobileItem')
    _mobile_data_tracking_locator = ('id', 'mobileCheck')
    _wifi_data_tracking_locator = ('id', 'wifiCheck')
    _mobile_data_label_locator = ('css selector', '#mobileItem label')
    _wifi_data_label_locator = ('css selector', '#wifiItem label')
    _wifi_overview_data_locator = ('id', 'wifiOverview')

    # usage app settings locators
    _settings_title_locator = ('css selector', 'section#settings-view h1')
    _settings_button_locator = ('css selector', 'button.settings-button')
    _settings_iframe_locator = ('id', "settings-view-placeholder")
    _reset_button_locator = ('id', 'reset-data-usage')
    _reset_confirm_locator = ('css selector', 'section#reset-confirmation-dialog button.danger')
    _done_button_locator = ('css selector', 'section#settings-view button#close-settings')

    # data alert section locators
    _data_alert_label_locator = ('css selector', 'ul.settings label.switch')
    _data_alert_switch_locator = ('css selector', 'input[data-option="dataLimit"]')
    _capacity_button_locator = ('css selector', '#data-limit-dialog form button')
    _size_input_locator = ('css selector', '#data-limit-dialog form input')
    _usage_done_button_locator = ('id', 'data-usage-done-button')

    # browser app locators
    _page_end_locator = ("id", "colophon")

    # notification bar locators
    _cost_control_widget_locator = ('css selector', 'iframe[data-frame-origin="app://costcontrol.gaiamobile.org"]')
    _data_usage_view_locator = ('id', 'datausage-limit-view')

    def setUp(self):
        GaiaTestCase.setUp(self)

        if self.wifi:
            self.data_layer.disable_wifi()
            self.data_layer.enable_cell_data()

        # launch the cost control app
        self.app = self.apps.launch('Usage')

    def test_cost_control_data_alert_mobile(self):
        # go through ftu if there is any, otherwise pass it
        try:
            # if there is fte coming up
            self.wait_for_element_displayed(*self._welcome_title_locator)

            # go through 1st step in fte
            self.wait_for_element_displayed(*self._welcome_title_locator)
            next = self.marionette.find_element(*self._next_button_locator_1)
            self.marionette.tap(next)

            # go through 2nd step in fte
            self.wait_for_element_displayed(*self._data_report_title_locator)
            next = self.marionette.find_element(*self._next_button_locator_2)
            self.marionette.tap(next)

            # go through final step in fte
            self.wait_for_element_displayed(*self._data_alert_title_locator)
            next = self.marionette.find_element(*self._go_button_locator)
            self.marionette.tap(next)
        except:
            # if there is no fte coming up
            pass

        # wait for usage app main screen to come out
        self.wait_for_element_displayed(*self._usage_app_main_locator)

        # make sure wifi tracking is on and mobile data tracking is off
        self.wait_for_element_displayed(*self._mobile_data_item_locator)
        mobileswitch = self.marionette.find_element(*self._mobile_data_tracking_locator)
        wifiswitch = self.marionette.find_element(*self._wifi_data_tracking_locator)
        mobileswitch_click = self.marionette.find_element(*self._mobile_data_label_locator)
        wifiswitch_click = self.marionette.find_element(*self._wifi_data_label_locator)
        if not mobileswitch.is_selected():
            self.marionette.tap(mobileswitch_click)
        if wifiswitch.is_selected():
            self.marionette.tap(wifiswitch_click)

        # go to settings section
        settings = self.marionette.find_element(*self._settings_button_locator)
        self.marionette.tap(settings)

        # go into iframe of usage app settings
        self.wait_for_element_displayed(*self._settings_iframe_locator)
        settings_iframe = self.marionette.find_element(*self._settings_iframe_locator)
        self.marionette.switch_to_frame(settings_iframe)

        # enable data use alert if not enabled
        # there is a bug that marionette 0.5.20 can't detect if some elements are displayed or not
        self.wait_for_element_displayed(*self._settings_title_locator)
        switch = self.marionette.find_element(*self._data_alert_switch_locator)

        if not switch.is_selected():
            self.marionette.tap(switch)

        # make sure the data alert is 0.1MB, or we would set it to 0.1MB
        detail_section = self.marionette.find_element('css selector', 'ul.settings button span')
        self.marionette.tap(detail_section)
        capacity = self.marionette.find_element(*self._capacity_button_locator)
        # there are two choice in this switch u'GB' or u'MB'. if it is u'GB', try to switch to u'MB'
        if capacity.text == u'GB':
            self.marionette.tap(capacity)
        # clear the default value and set it to 0.1
        size = self.marionette.find_element(*self._size_input_locator)
        size.clear()
        size.send_keys('0.1')
        done = self.marionette.find_element(*self._usage_done_button_locator)
        self.marionette.tap(done)

        # reset data
        self.wait_for_element_displayed(*self._settings_title_locator)
        reset = self.marionette.find_element(*self._reset_button_locator)
        self.marionette.tap(reset)
        self.wait_for_element_displayed(*self._reset_confirm_locator)
        confirm = self.marionette.find_element(*self._reset_confirm_locator)
        self.marionette.tap(confirm)

        # done with settings section
        self.wait_for_element_displayed(*self._done_button_locator)
        done = self.marionette.find_element(*self._done_button_locator)
        self.marionette.tap(done)

        # open browser to get some data downloaded
        # please remove this once there is a better way than launching browser app/obj to do so
        browser = Browser(self.marionette)
        browser.launch()
        browser.go_to_url('http://www.mozilla.org/')
        browser.switch_to_content()
        self.wait_for_element_present(*self._page_end_locator)
        browser.switch_to_chrome()

        # get the notification bar
        self.marionette.switch_to_frame()
        self.marionette.execute_script("window.wrappedJSObject.UtilityTray.show()")

        # switch to cost control widget
        usage_iframe = self.marionette.find_element(*self._cost_control_widget_locator)
        self.marionette.switch_to_frame(usage_iframe)

        # make sure the color changed
        bar = self.marionette.find_element(*self._data_usage_view_locator)
        self.wait_for_condition(lambda m: 'reached-limit' in bar.get_attribute('class'),
            message='Data usage bar did not breach limit')
