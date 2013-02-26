# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaStressTest

import os
import datetime
import time


class TestStressVideoPlayback(GaiaStressTest):

    # Video list/summary view
    _video_items_locator = ('css selector', 'ul#thumbnails li[data-name]')
    _video_name_locator = ('css selector', 'div.details')

    # Video player fullscreen
    _video_title_locator = ('id', 'video-title')
    _elapsed_text_locator = ('id', 'elapsed-text')
    _video_controls_locator = ('id', 'videoControls')

    def setUp(self):
        GaiaStressTest.setUp(self)

        # Set name of stress test method to be repeated
        self.test_method = self.video_playback

        # add video to storage
        self.push_resource('VID_0001.3gp', 'DCIM/100MZLLA')
     
    def test_stress_add_event(self):
        self.drive()

    def video_playback(self, count):
        # Playback existing video, most code taken from test_video_player.py

        # launch the Video app
        self.app = self.apps.launch('Video')
        self.wait_for_element_displayed(*self._video_items_locator)

        all_videos = self.marionette.find_elements(*self._video_items_locator)

        # Assert that there are more than one video available
        self.assertGreater(all_videos, 0)
        self.first_video = all_videos[0]
        self.first_video_name = self.first_video.find_element(*self._video_name_locator).get_attribute('data-raw')

        # click on the first video
        self.marionette.tap(self.first_video)

        # Tap on video to keep toolbar visible
        self.wait_for_element_displayed(*self._video_controls_locator)
        self.marionette.tap(self.marionette.find_element(*self._video_controls_locator))

        # The elapsed time != 0:00 is the only indication of the toolbar visible
        time.sleep(1)
        self.assertNotEqual(self.marionette.find_element(*self._elapsed_text_locator).text, "00:00")

        # Check the name too. This will only work if the toolbar is visible
        self.wait_for_element_displayed(*self._video_title_locator)
        self.assertEqual(self.first_video_name,
                         self.marionette.find_element(*self._video_title_locator).text)

        # Wait for playback to be complete
        self.wait_for_element_not_displayed(*self._video_title_locator)
        self.wait_for_element_not_displayed(*self._video_controls_locator)
        time.sleep(1)

        # Kill the app
        self.apps.kill(self.app)

        # Wait a couple of seconds before repeating
        time.sleep(2)
