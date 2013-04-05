# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from gaiatest import GaiaTestCase
from gaiatest.apps.browser.app import Browser


class TestCostControlReset(GaiaTestCase):

    # fte locators (can be removed once javascript starts to work)
    _welcome_title_locator = ('css selector', 'h1[data-l10n-id="fte-welcome-title"]')
    _next_button_locator_1 = ('css selector', 'section#step-1 span[data-l10n-id="next"]')
    _data_report_title_locator = ('css selector', 'h1[data-l10n-id="fte-onlydata2-title"]')
    _next_button_locator_2 = ('css selector', 'section#non-vivo-step-1 span[data-l10n-id="next"]')
    _data_alert_title_locator = ('css selector', 'section#non-vivo-step-2 h1[data-l10n-id="fte-onlydata3-title"]')
    _go_button_locator = ('css selector', 'section#non-vivo-step-2 button.recommend')

    # usage main screen locators
    _usage_app_main_locator = ('id', 'datausage-tab')
    _usage_app_title_locator = ('css selector', 'h1[data-l10n-id="usage"]')

    # main screen switch locators
    _mobile_data_item_locator = ('id', 'mobileItem')
    _mobile_data_tracking_locator = ('id', 'mobileCheck')
    _wifi_data_tracking_locator = ('id', 'wifiCheck')
    _mobile_data_label_locator = ('css selector', 'li#mobileItem label')
    _wifi_data_label_locator = ('css selector', 'li#wifiItem label')
    _wifi_overview_data_locator = ('id', 'wifiOverview')

    # browser app locators
    _page_title_locator = ("id", "page-title")

    # usage app settings app
    _settings_title_locator = ('css selector', 'section#settings-view h1')
    _settings_button_locator = ('css selector', 'button.settings-button')
    _settings_iframe_locator = ('id', "settings-view-placeholder")
    _reset_button_locator = ('id', 'reset-data-usage')
    _reset_confirm_locator = ('css selector', 'section#reset-confirmation-dialog button.danger')
    _done_button_locator = ('css selector', 'section#settings-view button#close-settings')

    _wifi_data_locator = ('css selector', 'p#wifi-data-usage span.usage')

    def setUp(self):
        GaiaTestCase.setUp(self)

        if self.wifi:
            self.data_layer.enable_wifi()
            self.data_layer.connect_to_wifi(self.testvars['wifi'])

        # launch the cost control app
        self.app = self.apps.launch('Usage')

    def test_cost_control_reset_wifi(self):
        # open fte from javascript (if this got fixed, switch to use fte:false and delete the temp solution down this section)
        # self.marionette.execute_script("return window.wrappedJSObject.ConfigManager.setOption({ fte: true });")
        # self.marionette.refresh()

        # temporary solution for current not working script (going through fte by UI)
        # please remove "fte locators" once this got fixed
        try:
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
            pass

        # wait for usage app main screen to come out
        self.wait_for_element_displayed(*self._usage_app_main_locator)

        # make sure wifi tracking is on and mobile data tracking is off
        self.wait_for_element_displayed(*self._mobile_data_item_locator)
        mobileswitch = self.marionette.find_element(*self._mobile_data_tracking_locator)
        wifiswitch = self.marionette.find_element(*self._wifi_data_tracking_locator)
        mobileswitch_click = self.marionette.find_element(*self._mobile_data_label_locator)
        wifiswitch_click = self.marionette.find_element(*self._wifi_data_label_locator)
        if mobileswitch.is_selected():
            self.marionette.tap(mobileswitch_click)
        if not wifiswitch.is_selected():
            self.marionette.tap(wifiswitch_click)

        # open browser to get some data downloaded
        # please remove this once there is a better way than launching browser app/obj to do so
        browser = Browser(self.marionette)
        browser.launch()
        browser.go_to_url('http://mozqa.com/data/firefox/layout/mozilla.html')
        browser.switch_to_content()
        self.wait_for_element_present(*self._page_title_locator)

        # go back to Usage app
        self.apps.launch('Usage')
        self.wait_for_element_displayed(*self._usage_app_title_locator)

        # if we can't trigger any data usage, there must be something wrong
        if self.marionette.find_element(*self._wifi_overview_data_locator).text == u'0.00 B':
            self.assertTrue(False, 'No data usage shown;')

        # disable wifi before reset data, wait for wifi to be closed, and switch back to self.app
        self.data_layer.forget_all_networks()
        self.data_layer.disable_wifi()
        time.sleep(1)
        self.marionette.switch_to_frame(self.app.frame)

        # go to settings section
        settings = self.marionette.find_element(*self._settings_button_locator)
        self.marionette.tap(settings)

        # go into iframe of usage app settings
        settings_iframe = self.marionette.find_element(*self._settings_iframe_locator)
        self.marionette.switch_to_frame(settings_iframe)

        # reset data
        self.wait_for_element_displayed(*self._settings_title_locator)
        reset = self.marionette.find_element(*self._reset_button_locator)
        self.marionette.tap(reset)
        self.wait_for_element_displayed(*self._reset_confirm_locator)
        confirm = self.marionette.find_element(*self._reset_confirm_locator)
        self.marionette.tap(confirm)
        self.wait_for_element_displayed(*self._done_button_locator)
        done = self.marionette.find_element(*self._done_button_locator)
        self.marionette.tap(done)

        # waiting for usage to be refreshed and checking for usage
        self.wait_for_condition(lambda m: m.find_element(*self._wifi_data_locator).text == u'0.00 B', message='Wifi usage did not re-set back to 0.00B')
