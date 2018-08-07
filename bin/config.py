# Python edgegrid module - CONFIG for ImgMan CLI module
""" Copyright 2017 Akamai Technologies, Inc. All Rights Reserved.
 
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

import sys, os

if sys.version_info[0] >= 3:
     # python3
     from configparser import ConfigParser
     import http.client as http_client
else:
     # python2.7
     from ConfigParser import ConfigParser
     import httplib as http_client

import argparse
import logging

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Process command line options.')

class EdgeGridConfig():

    def __init__(self, config_values, configuration, flags=None):

        subparsers = parser.add_subparsers(help='commands', dest="command")

        list_parser = subparsers.add_parser("list", help="List all Policies")

        retrieve_parser = subparsers.add_parser("retrieve", help="Retrieve a policy")
        retrieve_parser.add_argument('name', help="Policy name to retrieve", action='store')
        retrieve_parser.add_argument('network', help="Network to retrieve from (STAGING or PRODUCTION)", action='store', default='PRODUCTION')
                
        addpol_parser = subparsers.add_parser("add", help="Add a policy with default configuration to both networks")
        addpol_parser.add_argument('name', help="Policy name to add", action='store')

        update_parser = subparsers.add_parser("update", help="Update a policy from a JSON file")
        update_parser.add_argument('name', help="Policy name to update", action='store')
        update_parser.add_argument('input_file', type=argparse.FileType('rt'), help="JSON Config file")
        update_parser.add_argument('network', help="Network to update on (STAGING or PRODUCTION)", action='store', default='PRODUCTION')

        delete_parser = subparsers.add_parser("delete", help="Delete a policy (both networks) USE CAUTION")
        delete_parser.add_argument('name', help="Policy name to delete", action='store')

        parser.add_argument('--cache', '-c', default=False, action='count')
        parser.add_argument('--human_readable', '-r', default=False, action='count')
        parser.add_argument('--verbose', '-v', default=False, action='count')
        parser.add_argument('--debug', '-d', default=False, action='count')
        parser.add_argument('--edgerc', '-e', default='~/.edgerc')
        parser.add_argument('--section', '-s', action='store')
        parser.add_argument('--output_file', '-f', type=argparse.FileType('wt'), help=' Output file {list, retrieve}')

        required = parser.add_argument_group('Required arguments')
        required.add_argument('--policy_set', '-p', action='store',  required=True)
        
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
            	if key not in arguments or arguments[key] == None:
            		arguments[key] = value
        else:
            	print ("Missing configuration file.  Run python gen_edgerc.py to get your credentials file set up once you've provisioned credentials in LUNA.")
            	return None

        for option in arguments:
            setattr(self,option,arguments[option])

        self.create_base_url()

    def create_base_url(self):
        self.base_url = "https://%s" % self.host
