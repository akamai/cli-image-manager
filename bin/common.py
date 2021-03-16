#! /usr/bin/env python

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

 ****************************************************************
 * Image Manager CLI module by Javier Garza (jgarza@akamai.com) *
 * Based on https://github.com/brassic-lint/cli-imgman          *
 *       from Gareth Hughes                                     *
 ****************************************************************

"""
# Libraries commmon to python 2 and 3
from __future__ import print_function
import sys
import os
import logging
import random
import re
import requests
import json
import urllib
import texttable as tt
from future import standard_library
from future.builtins import next
from future.builtins import object
from http_calls import EdgeGridHttpCaller
from akamai.edgegrid import EdgeGridAuth
from config import EdgeGridConfig
from subprocess import call
standard_library.install_aliases()

if sys.version_info[0] >= 3:
     # python3
	from urllib.parse import urljoin
else:
     # python2.7
     from urlparse import urljoin

session = requests.Session()
debug = False
verbose = False
cache = False
format = "json"
section_name = "default"
network = "production"

# If all parameters are set already, use them.  Otherwise
# use the config
config = EdgeGridConfig({"verbose": False}, section_name)

if hasattr(config, "debug") and config.debug:
    debug = True

if hasattr(config, "verbose") and config.verbose:
    verbose = True

if hasattr(config, "cache") and config.cache:
    cache = True


# Set the config options
session.auth = EdgeGridAuth(
    client_token=config.client_token,
    client_secret=config.client_secret,
    access_token=config.access_token
)

if hasattr(config, 'headers'):
    session.headers.update(config.headers)

session.headers.update({'User-Agent': "AkamaiCLI"})

baseurl = '%s://%s/' % ('https', config.host)

HttpCaller = EdgeGridHttpCaller(session, debug, verbose, baseurl)



def listPolicies(lunaToken, network, account_key=''):
    """ List the policies on a given network """
    session.headers.update({'Luna-Token': lunaToken})

    list_endpoint = "/imaging/v2/network/" + network + "/policies"
    if account_key != '':
        list_endpoint = list_endpoint + '?accountSwitchKey=' + account_key

    listResult = HttpCaller.getResult(list_endpoint)
    return(listResult)


def getPolicy(lunaToken, policyName, network, account_key=''):
    """ Gets a specific policy on a given network in JSON format """
    session.headers.update({'Luna-Token': lunaToken})

    if network == 'staging':
        get_policy_endpoint = "/imaging/v2/network/staging/policies/" + policyName
    else:
        get_policy_endpoint = "/imaging/v2/network/production/policies/" + policyName   

    if account_key != '':
        get_policy_endpoint = get_policy_endpoint + '?accountSwitchKey=' + account_key    

    print("Retrieving: " + policyName + " from " + network)

    policyResult = HttpCaller.getResult(get_policy_endpoint)

    return(policyResult)


def setPolicy(lunaToken, policyName, policyData, network, account_key=''):
    """ Creates or updates a policy in a given network (or both) out of
    a JSON input file """
    session.headers.update({'Luna-Token': lunaToken, "Content-Type":
                            "application/json"})

    if network == 'staging':
        set_policy_endpoint = "/imaging/v2/network/staging/policies/" + policyName
    else:
        set_policy_endpoint = "/imaging/v2/network/production/policies/" + policyName


    if account_key != '':
        set_policy_endpoint = set_policy_endpoint + '?accountSwitchKey=' + account_key     

    print("Updating " + policyName)

    policyResult = HttpCaller.putResult(set_policy_endpoint, policyData)

    return(policyResult)


def deletePolicy(lunaToken, policyName, network, account_key=''):
    """ Deletes a policy in a given network (or both) """
    session.headers.update({'Luna-Token': lunaToken})

    del_policy_stg_endpoint = "/imaging/v2/network/staging/policies/" + policyName
    del_policy_prd_endpoint = "/imaging/v2/network/production/policies/" + policyName

    if account_key != '':
        del_policy_stg_endpoint = del_policy_stg_endpoint + '?accountSwitchKey=' + account_key     
        del_policy_prd_endpoint = del_policy_prd_endpoint + '?accountSwitchKey=' + account_key     

    print("deleting " + policyName + " on " + network + " networks")
    if network == "both":
        policyResultStg = HttpCaller.deleteResult(del_policy_stg_endpoint)
        policyResultPrd = HttpCaller.deleteResult(del_policy_prd_endpoint)
        policyResult = {"staging": policyResultStg, "production":
                        policyResultPrd}
    if network == "staging":
        policyResultStg = HttpCaller.deleteResult(del_policy_stg_endpoint)
        policyResult = {"staging": policyResultStg}
    if network == "production":
        policyResultPrd = HttpCaller.deleteResult(del_policy_prd_endpoint)
        policyResult = {"production": policyResultPrd}

    return(policyResult)


def formatOutput(policyList, output_type):
    """ Formats the output on a given format (json or text) """
    if output_type == "json":
        # Let's print the JSON
        print(json.dumps(policyList, indent=2))

    if output_type == "text":
        # Iterate over the dictionary and print the selected information
        ParentTable = tt.Texttable()
        ParentTable.set_cols_width([30,25,25])
        ParentTable.set_cols_align(['c','c','c'])
        ParentTable.set_cols_valign(['m','m','m'])
        Parentheader = ['Policy name','Date Created','User']
        ParentTable.header(Parentheader)
        for my_item in policyList["items"]:
            Parentrow = [ my_item["id"], my_item["dateCreated"], my_item["user"]]
            ParentTable.add_row(Parentrow)
        MainParentTable = ParentTable.draw()
        print(MainParentTable)
        """print('%30s | %25s | %20s' % ("Policy name", "Date Created", "User"))
        print('='*81)
        for my_item in policyList["items"]:
            print('%30s | %25s | %20s' % (my_item["id"],
                                          my_item["dateCreated"],
                                          my_item["user"]))
        """


def main():
    """ Processes the right command (list, get, set or delete) """
    if config.command == "list-policies":
        # Get the list of policies in JSON format for the given network
        print("Policy:", config.policy_set, "\tNetwork:", config.network,
              "\tOutput:", config.output_type)

        if config.network == "both":
            print("\nSTAGING:")
            policyList = listPolicies(config.policy_set, "staging", config.account_key)
            formatOutput(policyList, config.output_type)
            print("\nPRODUCTION:")
            policyList = listPolicies(config.policy_set, "production", config.account_key)
            formatOutput(policyList, config.output_type)
        else:
            policyList = listPolicies(config.policy_set, config.network, config.account_key)
            formatOutput(policyList, config.output_type)

    elif config.command == "get-policy":

        policyDetail = getPolicy(config.policy_set, config.name,
                                 config.network, config.account_key)
        print("Policy:", config.policy_set, "\tNetwork:", config.network,
              "\tOutput:", config.output_file)
        if hasattr(config, 'output_file') and config.output_file is not None:
            config.output_file.write(json.dumps(policyDetail, indent=2))
            config.output_file.close()
        else:
            print(json.dumps(policyDetail, indent=2))

    elif config.command == "set-policy":
        policyJSON = config.input_file.read()
        config.input_file.close()
        if config.network == "both":
            print("STAGING:")
            policyDetail = setPolicy(config.policy_set, config.name,
                                     policyJSON, "staging", config.account_key)
            print(json.dumps(policyDetail, indent=2))
            print("PRODUCTION:")
            policyDetail = setPolicy(config.policy_set, config.name,
                                     policyJSON, "production", config.account_key)
            print(json.dumps(policyDetail, indent=2))
        else:
            print(config.network)
            policyDetail = setPolicy(config.policy_set, config.name,
                                     policyJSON, config.network, config.account_key)
            print(json.dumps(policyDetail, indent=2))

    elif config.command == "delete-policy":
        cmdResult = deletePolicy(config.policy_set, config.name,
                                 config.network, config.account_key)
        print(json.dumps(cmdResult, indent=2))
    else:
        config.parser.print_help(sys.stderr)


if __name__ == "__main__":
    main()
