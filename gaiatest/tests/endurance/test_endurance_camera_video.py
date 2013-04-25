# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Approximate runtime per 100 iterations: XXX minutes

from gaiatest import GaiaEnduranceTest

import time


class TestEnduranceCameraVideo(GaiaEnduranceTest):

    _switch_source_button_locator = ('id', 'switch-button')
    _capture_button_enabled_locator = ('css selector', '#capture-button:not([disabled])')
    _capture_button_locator = ('id', 'capture-button')
    _video_capturing_locator = ('css selector', 'body.capturing')
    _video_timer_locator = ('id', 'video-timer')
    _film_strip_image_locator = ('css selector', '#filmstrip > img.thumbnail')

    def setUp(self):
        GaiaEnduranceTest.setUp(self)

        # Set name of endurance test method to be repeated
        self.test_method = self.camera_video

        # Specify name of gaia app under test (required for DataZilla)
        self.app_under_test = "camera"

        # Set video record duration
        self.duration = 7
        self.marionette.log("Video capture duration is " + str(self.duration) + " seconds")

        # Turn off geolocation prompt
        self.apps.set_permission('Camera', 'geolocation', 'deny')

    def test_endurance_camera_video(self):
        self.drive()

    def camera_video(self, count):
        # Start camera, capture video and verify a video was taken, close camera
        # Most of the code borrowed from test_camera.py
        self.app = self.apps.launch('camera')
        self.wait_for_element_present(*self._capture_button_enabled_locator)

        switch_source_button = self.marionette.find_element(*self._switch_source_button_locator)
        self.marionette.tap(switch_source_button)
        self.wait_for_element_present(*self._capture_button_enabled_locator)

        time.sleep(2)
        capture_button = self.marionette.find_element(*self._capture_button_locator)
        self.marionette.tap(capture_button)

        self.wait_for_element_present(*self._video_capturing_locator)

        # Wait for recording duration
        timer_text = "00:%02d" % self.duration

        self.wait_for_condition(lambda m: m.find_element(
            *self._video_timer_locator).text == timer_text, timeout = self.duration + 30)

        # Stop recording
        self.marionette.tap(capture_button)
        self.wait_for_element_not_displayed(*self._video_timer_locator)

        # Wait for image to be added in to filmstrip
        self.wait_for_element_displayed(*self._film_strip_image_locator, timeout=30)

        # Find new video in the film strip
        self.assertTrue(self.marionette.find_element(*self._film_strip_image_locator).is_displayed())
        
        # Sleep a bit
        time.sleep(2)

        # Close the app via home button
        self.close_app()

        # Wait between iterations
        time.sleep(3)
