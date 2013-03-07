# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Approximate runtime per 100 iterations: 23.5 minutes

from gaiatest import GaiaStressTest

import os
import datetime
import time


class TestStressCameraPhoto(GaiaStressTest):

    _capture_button_locator = ('id', 'capture-button')
    _focus_ring = ('id', 'focus-ring')
    _film_strip_image_locator = ('css selector', '#filmstrip > img.thumbnail')

    def setUp(self):
        GaiaStressTest.setUp(self)

        # Set name of stress test method to be repeated
        self.test_method = self.camera_photo

        # Turn off geolocation prompt
        self.apps.set_permission('Camera', 'geolocation', 'deny')

    def test_stress_camera_photo(self):
        self.drive()

    def camera_photo(self, count):
        # Start camera, take photo and verify a photo was taken, close camera
        # Code borrowed from test_camera.py
        self.app = self.apps.launch('camera')
        self.wait_for_capture_ready()

        capture_button = self.marionette.find_element(*self._capture_button_locator)
        self.marionette.tap(capture_button)

        # Wait to complete focusing
        self.wait_for_condition(lambda m: m.find_element(*self._focus_ring).get_attribute('data-state') == 'focused',
            message="Camera failed to focus")

        # Wait for image to be added in to filmstrip
        # TODO investigate lowering this timeout in the future
        self.wait_for_element_displayed(*self._film_strip_image_locator, timeout=20)

        # Find the new picture in the film strip
        self.assertTrue(self.marionette.find_element(*self._film_strip_image_locator).is_displayed())

        # Close the app using home button
        self.close_app()

        # Wait a couple of seconds before repeating
        time.sleep(2)

    def wait_for_capture_ready(self):
        self.marionette.set_script_timeout(10000)
        self.marionette.execute_async_script("""
            waitFor(
                function () { marionetteScriptFinished(); },
                function () { return document.getElementById('viewfinder').readyState > 1; }
            );
        """)
