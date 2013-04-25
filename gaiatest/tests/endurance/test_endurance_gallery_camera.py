# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Approximate runtime per 100 iterations: xxx minutes

import time

from gaiatest import GaiaEnduranceTest
from gaiatest.apps.gallery.app import Gallery


class TestEnduranceGalleryCamera(GaiaEnduranceTest):

    def setUp(self):
        GaiaEnduranceTest.setUp(self)

        # Set name of endurance test method to be repeated
        self.test_method = self.gallery_camera

        # Specify name of gaia app under test (required for DataZilla)
        self.app_under_test = "gallery"

        # Turn off geolocation prompt
        self.apps.set_permission('Camera', 'geolocation', 'deny')

        # add photo to storage
        self.push_resource('IMG_0001.jpg', destination='DCIM/100MZLLA')        

        self.gallery = Gallery(self.marionette)
        self.gallery.launch()
        self.gallery.wait_for_files_to_load(1)

    def test_endurance_gallery_camera(self):
        self.drive()

    def gallery_camera(self, count):
        # Test requested per bug 851626:
        # 1. open the Gallery app
        # 2. when the UI/Camera button appears, tap it to switch to the camera
        # 3. when the UI/Gallery button appears, tap it to switch back to the gallery
        # 4. repeat steps 2 and 3 until *crash*
        time.sleep(3)

        # From gallery app, switch to camera app
        self.gallery.switch_from_gallery_to_camera()
        time.sleep(3)

        # From camera app, switch back to gallery again
        self.gallery.switch_from_camera_to_gallery()
