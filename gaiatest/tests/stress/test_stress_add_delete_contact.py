# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaStressTest
from gaiatest.mocks.mock_contact import MockContact
import os
import time


class TestStressAddDeleteContact(GaiaStressTest):

    _loading_overlay = ('id', 'loading-overlay')

    # Header buttons
    _add_new_contact_button_locator = ('id', 'add-contact-button')
    _done_button_locator = ('id', 'save-button')
    _edit_contact_button_locator = ('id', 'edit-contact-button')
    _delete_contact_button_locator = ('id', 'delete-contact')
    

    # Delete confirmation dialog
    _confirm_dialog_locator = ('id', 'confirmation-message')
    _remove_button_locator = ('css selector', 'button.danger')
    
    # New/Edit contact fields
    _given_name_field_locator = ('id', 'givenName')
    _family_name_field_locator = ('id', 'familyName')
    _email_field_locator = ('id', "email_0")
    _phone_field_locator = ('id', "number_0")
    _street_field_locator = ('id', "streetAddress_0")
    _zip_code_field_locator = ('id', "postalCode_0")
    _city_field_locator = ('id', 'locality_0')
    _country_field_locator = ('id', 'countryName_0')
    _comment_field_locator = ('id', 'note_0')

    def setUp(self):
        GaiaStressTest.setUp(self)

        # Name of stress test method to be repeated
        self.test_method = self.add_delete_contact

        # Launch the Contacts app
        self.app = self.apps.launch('Contacts')
        self.wait_for_element_not_displayed(*self._loading_overlay)

        self.contact = MockContact()

    def test_stress_add_delete_contact(self):
        self.drive()

    def create_contact_locator(self, contact):
        return ('css selector', '.contact-item p[data-order^=%s]' % contact)

    def add_delete_contact(self, count):
        # Add a new contact, most of this code borrowed from test_add_new_contact
        # Uses data from mock contact, except adds iteration to first name

        # Click Create new contact
        self.wait_for_element_displayed(*self._add_new_contact_button_locator)
        add_new_contact = self.marionette.find_element(*self._add_new_contact_button_locator)
        self.marionette.tap(add_new_contact)
        self.wait_for_element_displayed(*self._given_name_field_locator)

        # Enter data into fields
        extra_text = "-%dof%d" % (count, self.iterations)
        self.marionette.find_element(*self._given_name_field_locator).send_keys(self.contact['givenName'] + extra_text)
        
        self.marionette.find_element(*self._family_name_field_locator).send_keys(self.contact['familyName'])

        self.marionette.find_element(
            *self._phone_field_locator).send_keys(self.contact['tel']['value'])
        self.marionette.find_element(
            *self._email_field_locator).send_keys(self.contact['email'])

        self.marionette.find_element(
            *self._street_field_locator).send_keys(self.contact['street'])
        self.marionette.find_element(
            *self._zip_code_field_locator).send_keys(self.contact['zip'])
        self.marionette.find_element(
            *self._city_field_locator).send_keys(self.contact['city'])
        self.marionette.find_element(
            *self._country_field_locator).send_keys(self.contact['country'])

        self.marionette.find_element(
            *self._comment_field_locator).send_keys(self.contact['comment'])

        done_button = self.marionette.find_element(*self._done_button_locator)
        self.marionette.tap(done_button)

        contact_locator = self.create_contact_locator(self.contact['givenName'] + extra_text)
        self.wait_for_element_displayed(*contact_locator)
      
        # Wait a couple of seconds
        time.sleep(2)

        # Open the contact
        contact_to_delete = self.marionette.find_element(*contact_locator)
        self.marionette.tap(contact_to_delete)

        # Click edit button
        self.wait_for_element_displayed(*self._edit_contact_button_locator)
        edit_contact_button = self.marionette.find_element(*self._edit_contact_button_locator)
        self.marionette.tap(edit_contact_button)        

        # Click delete button
        self.wait_for_element_displayed(*self._delete_contact_button_locator)
        delete_contact_button = self.marionette.find_element(*self._delete_contact_button_locator)
        self.marionette.tap(delete_contact_button)        

        # Click remove button to confirm the delete
        self.wait_for_element_displayed(*self._confirm_dialog_locator)
        self.wait_for_element_displayed(*self._remove_button_locator)
        confirm_remove_button = self.marionette.find_element(*self._remove_button_locator)
        self.marionette.tap(confirm_remove_button)

       # Bug 779284 is blocking this test; modalu pop-up dialog (delete confirmation) is not
       # supported by Marionette yet so cannot click the 'Remove' button to confirm the delete

        # Verify contact is no longer in the list
        self.wait_for_element_not_displayed(*contact_locator)

        # Wait a couple of seconds before the next iteration
        time.sleep(2)

    def create_contact_locator(self, contact):
        return ('xpath', "//a[descendant::strong[text()='%s']]" % contact)
