# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Approximate runtime per 100 iterations: xxx minutes

import time

from gaiatest import GaiaStressTest
from gaiatest.mocks.mock_contact import MockContact
from gaiatest.apps.contacts.app import Contacts


class TestStressAddContact(GaiaStressTest):

    def setUp(self):
        GaiaStressTest.setUp(self)

        # Name of stress test method to be repeated
        self.test_method = self.add_contact

        # Remove any existing contacts
        self.data_layer.remove_all_contacts(60000)

        # Launch the Contacts app
        self.contacts_app = Contacts(self.marionette)
        self.contacts_app.launch()

        self.contact = MockContact()

    def test_stress_add_contact(self):
        self.drive()

    def add_contact(self, count):
        # Add a new contact, most of this code borrowed from test_add_new_contact
        # Uses data from mock contact, except adds iteration to first name

        # Add new contact
        new_contact_form = self.contacts_app.tap_new_contact()

        # Enter data into fields
        extra_text = "-%dof%d" % (count, self.iterations)
        new_contact_form.type_given_name(self.contact['givenName'] + extra_text)
        new_contact_form.type_family_name(self.contact['familyName'])

        new_contact_form.type_phone(self.contact['tel']['value'])
        new_contact_form.type_email(self.contact['email'])
        new_contact_form.type_street(self.contact['street'])
        new_contact_form.type_zip_code(self.contact['zip'])
        new_contact_form.type_city(self.contact['city'])
        new_contact_form.type_country(self.contact['country'])
        new_contact_form.type_comment(self.contact['comment'])

        # Save new contact
        new_contact_form.tap_done()

        # Verify a new contact was added
        self.wait_for_condition(lambda m: len(self.contacts_app.contacts) == count)

        # Sleep between reps
        time.sleep(3)
