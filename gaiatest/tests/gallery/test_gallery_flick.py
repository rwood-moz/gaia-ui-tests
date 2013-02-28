# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
import time


class TestGallery(GaiaTestCase):

    _progress_bar_locator = ('id', 'progress')
    _gallery_items_locator = ('css selector', 'li.thumbnail')
    _current_image_locator = ('css selector', '#frames > div.frame[style ~= "translateX(0px);"] > img')
    _photos_toolbar_locator = ('id', 'fullscreen-toolbar')

    images = 'IMG_0001.jpg'
    image_count = 4

    def setUp(self):
        GaiaTestCase.setUp(self)

        # add photos to storage
        self.push_resource(self.images, self.image_count, 'DCIM/100MZLLA')

        # launch the Gallery app
        self.app = self.apps.launch('Gallery')

    def test_gallery_full_screen_image_flicks(self):
        # https://moztrap.mozilla.org/manage/case/1326/

        #wait for gallery to be available
        self.wait_for_element_not_displayed(*self._progress_bar_locator)

        all_gallery_items = self.marionette.find_elements(*self._gallery_items_locator)

        self.assertEqual(len(all_gallery_items), self.image_count)

        # tap first image to open full screen view
        self.marionette.tap(all_gallery_items[0])
        self.wait_for_element_displayed(*self._current_image_locator)

        previous_image_source = None

        # Check the next flicks
        for i in range(len(all_gallery_items)):

            current_image_source = self.marionette.find_element(*self._current_image_locator).get_attribute('src')

            self.assertIsNotNone(current_image_source)
            self.assertNotEqual(current_image_source, previous_image_source)

            self.assertTrue(self.is_element_displayed(*self._photos_toolbar_locator))

            previous_image_source = current_image_source

            self.flick_to_image('next')

        current_image_source = self.marionette.find_element(*self._current_image_locator).get_attribute('src')

        self.assertIsNotNone(current_image_source)
        self.assertEqual(current_image_source, previous_image_source)

        self.assertTrue(self.is_element_displayed(*self._photos_toolbar_locator))

        previous_image_source = current_image_source

        # check the prev flick
        for i in range(len(all_gallery_items) - 1):

            self.flick_to_image('previous')

            current_image_source = self.marionette.find_element(*self._current_image_locator).get_attribute('src')

            self.assertIsNotNone(current_image_source)
            self.assertNotEqual(current_image_source, previous_image_source)

            self.assertTrue(self.is_element_displayed(*self._photos_toolbar_locator))

            previous_image_source = current_image_source

        # try to flick prev image (No image should be available)
        self.flick_to_image('previous')

        current_image_source = self.marionette.find_element(*self._current_image_locator).get_attribute('src')

        self.assertIsNotNone(current_image_source)
        self.assertEqual(current_image_source, previous_image_source)

        self.assertTrue(self.is_element_displayed(*self._photos_toolbar_locator))

    def flick_to_image(self, direction):
        self.assertTrue(direction in ['previous', 'next'])
        current_image = self.marionette.find_element(*self._current_image_locator)
        self.marionette.flick(current_image,  # target element
                              '50%', '50%',  # start from middle of the target element
                              '%s50%%' % (direction == 'previous' and '+' or direction == 'next' and '-'), 0,  # move 50% of width to the left/right
                              800)  # gesture duration
        self.wait_for_element_displayed(*self._current_image_locator)
        time.sleep(1)
