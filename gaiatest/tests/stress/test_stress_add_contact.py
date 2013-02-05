# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.mocks.mock_contact import MockContact
import os


class TestStressAddContact(GaiaTestCase):

    _loading_overlay = ('id', 'loading-overlay')

    # Header buttons
    _add_new_contact_button_locator = ('id', 'add-contact-button')
    _done_button_locator = ('id', 'save-button')

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
        GaiaTestCase.setUp(self)

        try:
            self.min_iterations = self.testvars['stresstests']['min_iterations']
        except:
            self.min_iterations = 100

        # Set iterations, ensure at least at minimum
        try:
            self.iterations = self.testvars['stresstests']['add_contact_iterations']
            if (self.iterations < self.min_iterations):
                self.iterations = self.min_iterations
        except:
            self.iterations = self.min_iterations

        # Get checkpoint, if not specified just do one at start and end
        try:
            self.checkpoint_every = self.testvars['stresstests']['add_contact_checkpoint']
        except:
            # Not specified, so just do at start and end
            self.checkpoint_every = self.iterations
        
        # Launch the Contacts app
        self.app = self.apps.launch('Contacts')
        self.wait_for_element_not_displayed(*self._loading_overlay)

        self.contact = MockContact()

    def test_stress_add_contact(self):
        # Starting checkpoint
        self.checkpoint()

        # Actual test case iterations        
        for count in range(1, self.iterations + 1):
            self.marionette.log("Add contact iteration %d of %d" % (count, self.iterations))
            self.add_contact(count)
            # Checkpoint time?
            if ((count % self.checkpoint_every) == 0):
                self.checkpoint(count)

    def add_contact(self, count):
        # Add a new contact, most of this code borrowed from test_add_new_contact
        # Uses data from mock contact, except adds the iteration number as name prefix

        # Click Create new contact
        self.wait_for_element_displayed(*self._add_new_contact_button_locator)
        add_new_contact = self.marionette.find_element(*self._add_new_contact_button_locator)
        self.marionette.tap(add_new_contact)

        self.wait_for_element_displayed(*self._given_name_field_locator)

        # Enter data into fields
        #first_name = str(count) + "%dof%d" + str(self.iterations) + self.contact['givenName'], % (str(count), str(self.iterations))
        first_name = "%07dof%d" % (count, self.iterations) + self.contact['givenName']

        self.marionette.find_element(*self._given_name_field_locator).send_keys(first_name)
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

        contact_locator = self.create_contact_locator(first_name)
        self.wait_for_element_displayed(*contact_locator)

    def create_contact_locator(self, contact):
        return ('xpath', "//a[descendant::strong[text()='%s']]" % contact)
    
    def checkpoint(self, iteration = 0):
        self.marionette.log("Checkpoint")
        if iteration == 0:
            os.system("echo test_stress_add_contacts > checkpoint.log")
        text = "echo checkpoint at iteration %d: >> checkpoint.log" % iteration
        os.system(text)
        os.system("adb shell b2g-ps >> checkpoint.log")
