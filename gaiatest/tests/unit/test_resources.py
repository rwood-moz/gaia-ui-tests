# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestResources(GaiaTestCase):

    filename = 'IMG_0001.jpg'

    def test_push_resource(self):
        self.push_resource(self.filename)
        self.assertTrue(self.filename in self.data_layer.media_files)

    def test_push_multiple_resources(self):
        count = 5
        self.push_resource(self.filename, count)

        for i in range(1, count + 1):
            remote_filename = '_%s.'.join(iter(self.filename.split('.'))) % i
            self.assertTrue(remote_filename in self.data_layer.media_files)
