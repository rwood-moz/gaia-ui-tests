# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
import time
from gaiatest.apps.messages.app import Messages
from gaiatest.apps.camera.app import Camera


class TestSmsWithAttachments(GaiaTestCase):

    def test_sms_send(self):
        self.connect_to_network()
        _text_message_content = "Automated Test %s" % str(time.time())

        # launch the app
        self.messages = Messages(self.marionette)
        self.messages.launch()

        # click new message
        new_message = self.messages.tap_create_new_message()
        new_message.type_phone_number(self.testvars['carrier']['phone_number'])

        new_message.type_message(_text_message_content)
        select_attachment = new_message.tap_attachment()
        camera = select_attachment.tap_camera()

        # switch frame to camera iframe
        camera.switch_to_camera_frame()

        camera.wait_for_camera_ready()
        camera.tap_capture()
        camera.wait_for_select_button_displayed()
        camera.tap_select_button()

        # switch back to messages app frame
        self.messages.switch_to_messages_frame()

        #click send
        self.message_thread = new_message.tap_send()
        self.message_thread.wait_for_received_messages()

        # get the most recent listed and most recent received text message
        last_received_message = self.message_thread.received_messages[-1]
        last_message = self.message_thread.all_messages[-1]

        # Check the most recent received message has the same text content
        self.assertEqual(_text_message_content, last_received_message.text.strip('\n').strip())

        # Check that most recent message is also the most recent received message
        self.assertEqual(last_received_message.id, last_message.id)

        # Check that message has attachments
        self.assertTrue(last_message.has_attachments)
