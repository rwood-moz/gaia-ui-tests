# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase

from marionette.errors import NoSuchElementException


class TestEditMode(GaiaTestCase):

    _edit_mode_locator = ('css selector', 'body[data-mode="edit"]')

    def setUp(self):
        GaiaTestCase.setUp(self)

        self.homescreen = self.apps.launch('Homescreen')

    def test_access_and_leave_edit_mode(self):

        self._go_to_next_page()

        # go to edit mode.
        # TODO: activate edit mode using javascript, instead of long_press due to https://bugzilla.mozilla.org/show_bug.cgi?id=814425
        self._activate_edit_mode()

        #verify that the delete app icons appear
        self.assertTrue(self.is_element_present(*self._edit_mode_locator))

        #tap home button and verify that delete app icons are no longer visible
        self._touch_home_button()

        self.assertFalse(self.is_element_present(*self._edit_mode_locator))

    def _touch_home_button(self):
        self.marionette.switch_to_frame()
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('home'));")

    def _go_to_next_page(self):
        self.marionette.execute_script('window.wrappedJSObject.GridManager.goToNextPage()')

    def _activate_edit_mode(self):
        self.marionette.execute_script("window.wrappedJSObject.Homescreen.setMode('edit')")
