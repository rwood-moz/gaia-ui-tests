# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Approximate runtime per 100 iterations: xxx minutes

from gaiatest import GaiaStressTest

import time


class TestStressGalleryCamera(GaiaStressTest):

    _switch_to_camera_button_locator = ('id', 'thumbnails-camera-button')
    _camera_frame_locator = ('css selector', 'iframe[data-url="app://camera.gaiamobile.org/index.html"]')
    _switch_to_gallery_button_locator = ('id', 'gallery-button')

    def setUp(self):
        GaiaStressTest.setUp(self)

        # Set name of stress test method to be repeated
        self.test_method = self.gallery_camera

        # Turn off geolocation prompt
        self.apps.set_permission('Camera', 'geolocation', 'deny')

        # add photo to storage
        self.push_resource('IMG_0001.jpg', destination='DCIM/100MZLLA')        

        # Start gallery app
        self.app = self.apps.launch('Gallery')
        time.sleep(5)

    def test_stress_gallery_camera(self):
        self.drive()

    def gallery_camera(self, count):
        # Test requested per bug 851626:
        # 1. open the Gallery app
        # 2. when the UI/Camera button appears, tap it to switch to the camera
        # 3. when the UI/Gallery button appears, tap it to switch back to the gallery
        # 4. repeat steps 2 and 3 until *crash*

        # Switch to camera
        self.wait_for_element_displayed(*self._switch_to_camera_button_locator)
        switch_to_camera_button = self.marionette.find_element(*self._switch_to_camera_button_locator)
        self.marionette.tap(switch_to_camera_button)
        time.sleep(5)

        # Switch to top level then camera frame
        self.marionette.switch_to_frame()
        self.marionette.switch_to_frame(self.marionette.find_element(*self._camera_frame_locator))

        # Switch back to gallery
        self.wait_for_element_displayed(*self._switch_to_gallery_button_locator)
        switch_to_gallery_button = self.marionette.find_element(*self._switch_to_gallery_button_locator)
        self.marionette.tap(switch_to_gallery_button)
        
        # Switch to top level then gallery
        self.marionette.switch_to_frame()
        self.marionette.switch_to_frame(self.app.frame)
        time.sleep(5)
