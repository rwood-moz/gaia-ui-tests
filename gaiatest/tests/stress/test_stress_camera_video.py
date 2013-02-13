# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaStressTest

import os
import datetime
import time


class TestStressCameraVideo(GaiaStressTest):

    _switch_source_button_locator = ('id', 'switch-button')
    _capture_button_enabled_locator = ('css selector', '#capture-button:not([disabled])')
    _capture_button_locator = ('id', 'capture-button')
    _video_capturing_locator = ('css selector', 'body.capturing')
    _video_timer_locator = ('id', 'video-timer')
    _film_strip_image_locator = ('css selector', '#filmstrip > img.thumbnail')

    def setUp(self):
        GaiaStressTest.setUp(self)

        # Set name of stress test method to be repeated
        self.test_method = self.camera_video

        # Get video recording duration in seconds, if not present default
        try:
            self.duration = self.testvars['stresstests']['camera_video']['capture_duration']
        except:
            # Not specified, so just do at start and end
            self.duration = 3

        # Currently this test restricts video capture duration to 3 seconds min and 59 seconds max
        if (self.duration > 59):
            self.duration = 59
        elif (self.duration < 3):
            self.duration = 3

        self.marionette.log("Video capture duration is " + str(self.duration) + " seconds")

        # Turn off geolocation prompt
        self.apps.set_permission('Camera', 'geolocation', 'deny')

    def test_stress_camera_video(self):
        self.drive()

    def camera_video(self, count):
        # Start camera, capture video and verify a video was taken, close camera
        # Most of the code borrowed from test_camera.py
        self.app = self.apps.launch('camera')
        self.wait_for_capture_ready()

        switch_source_button = self.marionette.find_element(*self._switch_source_button_locator)

        self.marionette.tap(switch_source_button)
        self.wait_for_element_present(*self._capture_button_enabled_locator)

        capture_button = self.marionette.find_element(*self._capture_button_locator)
        self.marionette.tap(capture_button)

        self.wait_for_element_present(*self._video_capturing_locator)

        # Wait for recording duration
        timer_text = "00:%02d" % self.duration

        self.wait_for_condition(lambda m: m.find_element(
            *self._video_timer_locator).text == timer_text, timeout = self.duration + 5)

        # Stop recording
        self.marionette.tap(capture_button)
        self.wait_for_element_not_displayed(*self._video_timer_locator)

        # Wait for image to be added in to filmstrip
        self.wait_for_element_displayed(*self._film_strip_image_locator)

        # Find the new film thumbnail in the film strip
        self.assertTrue(self.marionette.find_element(*self._film_strip_image_locator).is_displayed())

        # Close the app
        self.apps.kill(self.app)        

    def wait_for_capture_ready(self):
        self.marionette.set_script_timeout(10000)
        self.marionette.execute_async_script("""
            waitFor(
                function () { marionetteScriptFinished(); },
                function () { return document.getElementById('viewfinder').readyState > 1; }
            );
        """)
