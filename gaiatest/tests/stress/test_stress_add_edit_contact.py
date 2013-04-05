# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Approximate runtime per 100 iterations: xxx minutes

from gaiatest import GaiaStressTest
from gaiatest.mocks.mock_contact import MockContact
import os
import time


class TestStressAddEditContact(GaiaStressTest):

    _loading_overlay = ('id', 'loading-overlay')

    # Header buttons
    _add_new_contact_button_locator = ('id', 'add-contact-button')
    _done_button_locator = ('id', 'save-button')
    _edit_contact_button_locator = ('id', 'edit-contact-button')
    _back_button_locator = ('id', 'details-back')

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
        self.test_method = self.add_edit_contact

        # Remove any existing contacts
        self.data_layer.remove_all_contacts(60000)

        # Launch the Contacts app
        self.app = self.apps.launch('Contacts')
        self.wait_for_element_not_displayed(*self._loading_overlay)

        self.contact = MockContact()

    def test_stress_add_edit_contact(self):
        self.drive()

    def create_contact_locator(self, contact):
        return ('css selector', '.contact-item p[data-order^=%s]' % contact)

    def add_edit_contact(self, count):
        # Add a new contact, most of this code borrowed from test_add_new_contact
        # Uses data from mock contact, except adds iteration to first name

        # Click Create new contact
        self.wait_for_element_displayed(*self._add_new_contact_button_locator)
        add_new_contact = self.marionette.find_element(*self._add_new_contact_button_locator)
        self.marionette.tap(add_new_contact)
        self.wait_for_element_displayed(*self._given_name_field_locator)

        # Enter data into fields
        count_text = "-%dof%d" % (count, self.iterations)
        self.marionette.find_element(*self._given_name_field_locator).send_keys(self.contact['givenName'] + count_text)
        time.sleep(1)
        self.marionette.find_element(*self._family_name_field_locator).send_keys(self.contact['familyName'])
        time.sleep(1)
        self.marionette.find_element(
            *self._phone_field_locator).send_keys(self.contact['tel']['value'])
        time.sleep(1)           
        self.marionette.find_element(
            *self._email_field_locator).send_keys(self.contact['email'])
        time.sleep(1)
        self.marionette.find_element(
            *self._street_field_locator).send_keys(self.contact['street'])
        time.sleep(1)           
        self.marionette.find_element(
            *self._zip_code_field_locator).send_keys(self.contact['zip'])
        time.sleep(1)            
        self.marionette.find_element(
            *self._city_field_locator).send_keys(self.contact['city'])
        time.sleep(1)           
        self.marionette.find_element(
            *self._country_field_locator).send_keys(self.contact['country'])
        time.sleep(1)
        self.marionette.find_element(
            *self._comment_field_locator).send_keys(self.contact['comment'])
        time.sleep(1)
        done_button = self.marionette.find_element(*self._done_button_locator)
        self.marionette.tap(done_button)
        time.sleep(1)

        contact_locator = self.create_contact_locator(self.contact['givenName'] + count_text)
        self.wait_for_element_displayed(*contact_locator)

        # Wait a bit before editing
        time.sleep(2)

        # Open the contact
        contact_to_delete = self.marionette.find_element(*contact_locator)
        self.marionette.tap(contact_to_delete)

        # Click edit button
        time.sleep(1)
        self.wait_for_element_displayed(*self._edit_contact_button_locator)
        edit_contact_button = self.marionette.find_element(*self._edit_contact_button_locator)
        self.marionette.tap(edit_contact_button)

        # Add 'mod' to first name
        time.sleep(1)
        self.wait_for_element_displayed(*self._given_name_field_locator)
        edit_text = "-edit"
        self.marionette.find_element(*self._given_name_field_locator).send_keys(edit_text)

        # Click update to save
        time.sleep(1)
        done_button = self.marionette.find_element(*self._done_button_locator)
        self.marionette.tap(done_button)

        # Contact is still displayed, go back to main contacts list
        time.sleep(1)
        self.wait_for_element_displayed(*self._back_button_locator)
        back_button = self.marionette.find_element(*self._back_button_locator)
        self.marionette.tap(back_button)

        # Find contact based on edited first name
        contact_locator = self.create_contact_locator(self.contact['givenName'] + count_text + edit_text)
        self.wait_for_element_displayed(*contact_locator)

        # Sleep between reps
        time.sleep(3)
