# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Approximate runtime per 100 iterations: 23.5 minutes

from gaiatest import GaiaEnduranceTest

import os
import datetime
import time


class TestEnduranceCameraPhoto(GaiaEnduranceTest):

    _capture_button_enabled_locator = ('css selector', '#capture-button:not([disabled])')
    _capture_button_locator = ('id', 'capture-button')
    _focus_ring = ('id', 'focus-ring')
    _film_strip_image_locator = ('css selector', '#filmstrip > img.thumbnail')

    def setUp(self):
        GaiaEnduranceTest.setUp(self)

        # Set name of endurance test method to be repeated
        self.test_method = self.camera_photo

        # Specify name of gaia app under test (required for DataZilla)
        self.app_under_test = "camera"

        # Turn off geolocation prompt
        self.apps.set_permission('Camera', 'geolocation', 'deny')

    def test_endurance_camera_photo(self):
        self.drive()

    def camera_photo(self, count):
        # Start camera, take photo and verify a photo was taken, close camera
        # Code borrowed from test_camera.py
        self.app = self.apps.launch('camera')
        self.wait_for_element_present(*self._capture_button_enabled_locator)        

        time.sleep(2)
        capture_button = self.marionette.find_element(*self._capture_button_locator)
        self.marionette.tap(capture_button)

        # Wait to complete focusing
        self.wait_for_condition(lambda m: m.find_element(*self._focus_ring).get_attribute('data-state') == 'focused',
            message="Camera failed to focus")

        # Wait for image to be added in to filmstrip
        self.wait_for_element_displayed(*self._film_strip_image_locator, timeout=30)

        # Find the new picture in the film strip
        self.assertTrue(self.marionette.find_element(*self._film_strip_image_locator).is_displayed())

        # Sleep a bit
        time.sleep(2)

        # Close the app using home button
        self.close_app()

        # Sleep between iterations
        time.sleep(5)
