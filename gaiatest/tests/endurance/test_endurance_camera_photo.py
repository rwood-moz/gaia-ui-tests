# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Approximate runtime per 100 iterations: xxx minutes

from gaiatest import GaiaEnduranceTest
from gaiatest.apps.camera.app import Camera

import time


class TestEnduranceCameraPhoto(GaiaEnduranceTest):

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
        # Start camera
        camera_app = Camera(self.marionette)
        camera_app.launch()
        time.sleep(5)

        # Take a photo, verify filmstrip
        camera_app.capture_photo()
        self.assertTrue(camera_app.is_filmstrip_image_displayed())

        # Sleep a bit then close the app
        time.sleep(5)
        self.close_app()

        # Sleep between iterations
        time.sleep(5)
