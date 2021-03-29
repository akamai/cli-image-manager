# Python edgegrid module - CONFIG for ImgMan CLI module
""" Copyright 2021 Akamai Technologies, Inc. All Rights Reserved.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.

 You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import sys
import os
import argparse
import logging

if sys.version_info[0] >= 3:
    # python3
    from configparser import ConfigParser
    import http.client as http_client
else:
    # python2.7
    from ConfigParser import ConfigParser
    import httplib as http_client

PACKAGE_VERSION = "0.1.8"

logger = logging.getLogger(__name__)

class EdgeGridConfig():

    parser = argparse.ArgumentParser(description='Process command line options.')

    def __init__(self, config_values, configuration, flags=None):
        parser = self.parser
        subparsers = parser.add_subparsers(help='commands', dest="command")

        list_parser = subparsers.add_parser("list-policies", help="List all Policies")
        list_parser.add_argument('--network', '-n', help="Network to list from (staging, production or both). Default is both", metavar='network', action='store', choices=['staging', 'production','both'],default='both')
        list_parser.add_argument('--output-type', '-t', default='text', choices=['json', 'text'],metavar='json/text', help=' Output type {json, text}. Default is text')

        get_parser = subparsers.add_parser("get-policy", help="Gets a specific policy")
        get_parser.add_argument('name', help="Policy name to retrieve", action='store')
        get_parser.add_argument('--network', '-n', help="Network to list from (staging or production). Default is production", metavar='network', action='store', choices=['staging', 'production'],default='production')
        get_parser.add_argument('--output-file', '-f', type=argparse.FileType('wt'), metavar='file_name', help=' Save output to a file')

        update_parser = subparsers.add_parser("set-policy", help="Add or updates a given policy out of a JSON file")
        update_parser.add_argument('name', help="Policy name to update", action='store')
        update_parser.add_argument('--input-file', '-f', type=argparse.FileType('rt'), required=True, metavar='filename', help="JSON Config file")
        update_parser.add_argument('--network', '-n', help="Network where the policy resides (staging, production or both). Default is production", metavar='network', action='store', choices=['staging', 'production','both'],default='production')

        delete_parser = subparsers.add_parser("delete-policy", help="Deletes a policy")
        delete_parser.add_argument('name', help="Policy name to delete", action='store')
        delete_parser.add_argument('--network', '-n', help="Network to delete from (staging, production or both). Default is production", metavar='network', action='store', choices=['staging', 'production','both'],default='production')

        parser.add_argument('--verbose', default=False, action='count', help=' Verbose mode')
        parser.add_argument('--version', '-v', default=False, action='version', version='version ' + PACKAGE_VERSION, help=' Version number')
        parser.add_argument('--debug', '-d', default=False, action='count', help=' Debug mode (prints HTTP headers)')
        parser.add_argument('--edgerc', '-e', default='~/.edgerc', metavar='credentials_file', help=' Location of the credentials file (default is ~/.edgerc)')
        parser.add_argument('--section', '-c', default='image-manager', metavar='credentials_file_section', action='store', help=' Credentials file Section\'s name to use')
        parser.add_argument('--policy-set', '-p', action='store', metavar='im_policy_name', required=True, help=' Image Manager Policy Name (as indicated in Property Manager and IM Policy Manager)')
        parser.add_argument('--account-key', '-a', default='', action='store', metavar='account_switch_key', required=True, help=' Account Switch Key for Internal Users')
        # parser.add_argument('--lookup-policy-set', '-l', action='store', metavar='property_name', help=' Lookup Image Manager Policy Name (by Property name)')
        # parser.add_argument('--session', '-s', default=False, action='store', help=' Session name (see: https://github.com/akamai/cli-image-manager#sessions)')

        if flags:
            for argument in flags.keys():
                parser.add_argument('--' + argument, action=flags[argument])

        arguments = {}
        for argument in config_values:
            if config_values[argument]:
                if config_values[argument] == "False" or config_values[argument] == "True":
                    parser.add_argument('--' + argument, action='count')
                parser.add_argument('--' + argument)
                arguments[argument] = config_values[argument]

        try:
            args = parser.parse_args()
        except:
            sys.exit()

        arguments = vars(args)

        if arguments['debug']:
            http_client.HTTPConnection.debuglevel = 1
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True

        if arguments['version']:
            print("Version: " + PACKAGE_VERSION)
            sys.exit()

        if "section" in arguments and arguments["section"]:
            configuration = arguments["section"]

        arguments["edgerc"] = os.path.expanduser(arguments["edgerc"])

        if os.path.isfile(arguments["edgerc"]):
            config = ConfigParser()
            config.readfp(open(arguments["edgerc"]))
            if not config.has_section(configuration):
                err_msg = "ERROR: No section named %s was found in your %s file\n" % (configuration, arguments["edgerc"])
                err_msg += "ERROR: Please generate credentials for the script functionality\n"
                err_msg += "ERROR: and run 'python gen_edgerc.py %s' to generate the credential file\n" % configuration
                sys.exit( err_msg )
            for key, value in config.items(configuration):
                # ConfigParser lowercases magically
                if key not in arguments or arguments[key] is None:
                    arguments[key] = value
                else:
                    print("Missing configuration file.  Run python gen_edgerc.py to get your credentials file set up once you've provisioned credentials in LUNA.")
                    return None

        for option in arguments:
            setattr(self, option, arguments[option])

        self.create_base_url()

    def create_base_url(self):
        self.base_url = "https://%s" % self.host
