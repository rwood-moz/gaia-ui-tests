#!/usr/bin/env python
#
# Before running this:
# 1) Install a B2G build with Marionette enabled
# 2) adb forward tcp:2828 tcp:2828

from optparse import OptionParser
from StringIO import StringIO
import os
#import pkg_resources
#import sys
#import time
from urlparse import urlparse
import xml.dom.minidom
import zipfile

#from progressbar import Counter
#from progressbar import ProgressBar

import dzclient
import gaiatest
from marionette import Marionette
#from marionette import MarionetteTouchMixin
import mozdevice


class DatazillaPerfPoster(object):

    def __init__(self, marionette, datazilla_config=None, sources=None):
        self.marionette = marionette

        settings = gaiatest.GaiaData(self.marionette).all_settings  # get all settings
        mac_address = self.marionette.execute_script('return navigator.mozWifiManager && navigator.mozWifiManager.macAddress;')

        #self.submit_report = True
        self.submit_report = False
        self.ancillary_data = {}

        if gaiatest.GaiaDevice(self.marionette).is_android_build:
            # get gaia, gecko and build revisions
            try:
                device_manager = mozdevice.DeviceManagerADB()
                app_zip = device_manager.pullFile('/data/local/webapps/settings.gaiamobile.org/application.zip')
                with zipfile.ZipFile(StringIO(app_zip)).open('resources/gaia_commit.txt') as f:
                    self.ancillary_data['gaia_revision'] = f.read().splitlines()[0]
            except zipfile.BadZipfile:
                # the zip file will not exist if Gaia has not been flashed to
                # the device, so we fall back to the sources file
                pass

            try:
                sources_xml = sources and xml.dom.minidom.parse(sources) or xml.dom.minidom.parseString(device_manager.catFile('system/sources.xml'))
                for element in sources_xml.getElementsByTagName('project'):
                    path = element.getAttribute('path')
                    revision = element.getAttribute('revision')
                    if not self.ancillary_data.get('gaia_revision') and path in 'gaia':
                        self.ancillary_data['gaia_revision'] = revision
                    if path in ['gecko', 'build']:
                        self.ancillary_data['_'.join([path, 'revision'])] = revision
            except:
                pass

        self.required = {
            'gaia revision': self.ancillary_data.get('gaia_revision'),
            'gecko revision': self.ancillary_data.get('gecko_revision'),
            'build revision': self.ancillary_data.get('build_revision'),
            'protocol': datazilla_config['protocol'],
            'host': datazilla_config['host'],
            'project': datazilla_config['project'],
            'branch': datazilla_config['branch'],
            'oauth key': datazilla_config['oauth_key'],
            'oauth secret': datazilla_config['oauth_secret'],
            'machine name': mac_address or 'unknown',
            'os version': settings.get('deviceinfo.os'),
            'id': settings.get('deviceinfo.platform_build_id')}

        for key, value in self.required.items():
            if not value:
                self.submit_report = False
                print 'Missing required DataZilla field: %s' % key

        if not self.submit_report:
            print 'Reports will not be submitted to DataZilla'

    def post_to_datazilla(self, results, app_name):
        # Prepare DataZilla results
        res = dzclient.DatazillaResult()
        test_suite = app_name.replace(' ', '_').lower()
        res.add_testsuite(test_suite)
        for metric in results.keys():
            res.add_test_results(test_suite, metric, results[metric])
        req = dzclient.DatazillaRequest(
            protocol=self.required.get('protocol'),
            host=self.required.get('host'),
            project=self.required.get('project'),
            oauth_key=self.required.get('oauth key'),
            oauth_secret=self.required.get('oauth secret'),
            machine_name=self.required.get('machine name'),
            os='Firefox OS',
            os_version=self.required.get('os version'),
            platform='Gonk',
            build_name='B2G',
            version='prerelease',
            revision=self.ancillary_data.get('gaia_revision'),
            branch=self.required.get('branch'),
            id=self.required.get('id'))

        # Send DataZilla results
        req.add_datazilla_result(res)
        for dataset in req.datasets():
            dataset['test_build'].update(self.ancillary_data)
            print 'Submitting results to DataZilla: %s' % dataset
            response = req.send(dataset)
            print 'Response: %s' % response.read()


class dzOptionParser(OptionParser):
    def __init__(self, **kwargs):
        OptionParser.__init__(self, **kwargs)
        self.add_option('--file',
                        action='store',
                        dest='results_file',
                        metavar='str',
                        help='Json checkpoint results file from the stress test')
        self.add_option('--dz-url',
                        action='store',
                        dest='datazilla_url',
                        default='https://datazilla.mozilla.org',
                        metavar='str',
                        help='datazilla server url (default: %default)')
        self.add_option('--dz-project',
                        action='store',
                        dest='datazilla_project',
                        metavar='str',
                        help='datazilla project name')
        self.add_option('--dz-branch',
                        action='store',
                        dest='datazilla_branch',
                        metavar='str',
                        help='datazilla branch name')
        self.add_option('--dz-key',
                        action='store',
                        dest='datazilla_key',
                        metavar='str',
                        help='oauth key for datazilla server')
        self.add_option('--dz-secret',
                        action='store',
                        dest='datazilla_secret',
                        metavar='str',
                        help='oauth secret for datazilla server')
        self.add_option('--sources',
                        action='store',
                        dest='sources',
                        metavar='str',
                        help='path to sources.xml containing project revisions')

    def datazilla_config(self, options):
        if options.sources:
            if not os.path.exists(options.sources):
                raise Exception('--sources file does not exist')

        datazilla_url = urlparse(options.datazilla_url)
        datazilla_config = {
            'protocol': datazilla_url.scheme,
            'host': datazilla_url.hostname,
            'project': options.datazilla_project,
            'branch': options.datazilla_branch,
            'oauth_key': options.datazilla_key,
            'oauth_secret': options.datazilla_secret}
        return datazilla_config


def cli():
    parser = dzOptionParser(usage='%prog file [options]')
    options, args = parser.parse_args()

    # Ensure have all required options
    if not options.results_file:
        parser.print_help()
        parser.exit()
        
    print 'CONTINUE CHECK OTHER OPTS EXIST!'

    # Ensure results file exists
    if not os.path.exists(options.results_file):
        raise Exception('%s file does not exist' %options.results_file)

    datazilla_config = parser.datazilla_config(options)
   
        
if __name__ == '__main__':
    cli()
