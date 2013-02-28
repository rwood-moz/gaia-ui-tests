# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.mocks.mock_contact import MockContact


class TestContacts(GaiaTestCase):

    _loading_overlay = ('id', 'loading-overlay')
    _contacts_frame_locator = ('css selector', "iframe[src='app://communications.gaiamobile.org/contacts/index.html']")

    # Header buttons
    _edit_contact_button_locator = ('id', 'edit-contact-button')
    _done_button_locator = ('id', 'save-button')

    # Contact details panel
    _contact_name_title = ('id', 'contact-name-title')
    _contact_image = ('id', 'cover-img')

    # New/Edit contact fields
    _contact_form_title = ('id', 'contact-form-title')
    _add_picture_link_locator = ('id', 'thumbnail-photo')

    # Select from: dialog
    _gallery_button_locator = ('xpath', "//a[text()='Gallery']")

    # Gallery
    _gallery_frame_locator = ('css selector', "iframe[src='app://gallery.gaiamobile.org/index.html#pick']")
    _gallery_items_locator = ('css selector', 'li.thumbnail')
    _gallery_crop_done_button_locator = ('id', 'crop-done-button')

    def setUp(self):
        GaiaTestCase.setUp(self)

        self.contact = MockContact()
        self.data_layer.insert_contact(self.contact)

        # add photo to storage
        self.push_resource('IMG_0001.jpg', destination='DCIM/100MZLLA')

        # launch the Contacts app
        self.app = self.apps.launch('Contacts')
        self.wait_for_element_not_displayed(*self._loading_overlay)

    def create_contact_locator(self, contact):
        return ('xpath', "//li[@class='contact-item']/a[p[contains(@data-search, '%s')]]" % contact)

    def test_add_photo_from_gallery_to_contact(self):
        # https://moztrap.mozilla.org/manage/case/5551/

        contact_locator = self.create_contact_locator(self.contact['givenName'])
        self.wait_for_element_displayed(*contact_locator)

        contact_listing = self.marionette.find_element(*contact_locator)
        self.marionette.tap(contact_listing)

        self.wait_for_element_displayed(*self._contact_name_title)
        full_name = self.contact['givenName'] + " " + self.contact['familyName']
        self.assertEqual(full_name, self.marionette.find_element(*self._contact_name_title).text)
        contact_image = self.marionette.find_element(*self._contact_image)
        saved_contact_image_style = contact_image.get_attribute('style')

        edit_contact = self.marionette.find_element(*self._edit_contact_button_locator)
        self.marionette.tap(edit_contact)
        self.wait_for_element_displayed(*self._contact_form_title)
        self.assertEqual('Edit contact', self.marionette.find_element(*self._contact_form_title).text)

        self.wait_for_element_displayed(*self._add_picture_link_locator)
        picture_link = self.marionette.find_element(*self._add_picture_link_locator)
        saved_picture_style = picture_link.get_attribute('style')
        self.marionette.tap(picture_link)

        # switch to the system app
        self.marionette.switch_to_frame()

        # choose the source as gallery app
        self.wait_for_element_displayed(*self._gallery_button_locator)
        self.marionette.tap(self.marionette.find_element(*self._gallery_button_locator))

        # switch to the gallery app
        self.wait_for_element_displayed(*self._gallery_frame_locator)
        self.marionette.switch_to_frame(self.marionette.find_element(*self._gallery_frame_locator))

        self.wait_for_element_displayed(*self._gallery_items_locator)
        gallery_items = self.marionette.find_elements(*self._gallery_items_locator)
        self.assertGreater(len(gallery_items), 0, 'No photos were found in the gallery.')
        self.marionette.tap(gallery_items[0])

        self.wait_for_element_displayed(*self._gallery_crop_done_button_locator)
        self.marionette.tap(self.marionette.find_element(*self._gallery_crop_done_button_locator))

        # switch back to the contacts app
        self.marionette.switch_to_frame()
        self.wait_for_element_displayed(*self._contacts_frame_locator)
        self.marionette.switch_to_frame(self.marionette.find_element(*self._contacts_frame_locator))
        self.wait_for_element_displayed(*self._contact_form_title)
        self.assertEqual('Edit contact', self.marionette.find_element(*self._contact_form_title).text)

        new_picture_style = self.marionette.find_element(*self._add_picture_link_locator).get_attribute('style')
        self.assertNotEqual(new_picture_style, saved_picture_style,
                            'The picture associated with the contact was not changed.')

        done_button = self.marionette.find_element(*self._done_button_locator)
        self.marionette.tap(done_button)
        self.wait_for_element_displayed(*self._contact_name_title)
        self.assertEqual(full_name, self.marionette.find_element(*self._contact_name_title).text)
        new_contact_image_style = self.marionette.find_element(*self._contact_image)
        self.assertNotEqual(new_picture_style, saved_contact_image_style,
                            'The picture associated with the contact was not changed.')