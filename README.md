# Akamai CLI: Image Manager Module

This module enables the use of Image Manager in the Akamai CLI tool

## Install

To install, use [Akamai CLI](https://github.com/akamai/cli):

```
akamai install imaging
```

You may also use this as a stand-alone command by downloading the
[latest release binary](https://github.com/akamai/cli-imaging/releases)
for your system, or by cloning this repository and compiling it yourself.

## Usage

```
akamai imaging [global flags] --policy_set POLICY_SET command 
```

## Global Flags
- `--edgerc value` — Location of the credentials file (default: user's directory like "/Users/jgarza") [$AKAMAI_EDGERC]
- `--section value` — Section of the credentials file (default: "imaging") [$AKAMAI_EDGERC_SECTION]
- `--debug` - `-d` - prints debug information
- `--verbose` - Print verbose information
- `--version`, `-v` — Print the version
- `--help`, `-h` — Show help

## Commands  
- `list` — List existing policies on given network, or both (default). Output can be formatted as json, HTML table or text (default); which is a human readable ascii table showing the policy name, creation date and creation user (useful for inventoring purposes).
- `get` — Retrieves a given policy on a given network (output can be saved into a file)
- `set` - Creates or updates a given policy on a given network (or both) using the JSON provided on a given input file 
- `delete` - Deletes a policy (given network or both)

Required arguments:
  --policy_set POLICY_SET, -p POLICY_SET

## Examples

### Listing

#### list Help

Showing the syntax
```
$ akamai imaging --section devrel-imaging --policy_set jgarza_sandbox_akamaideveloper_com-10526224 list --help

usage: akamai-imaging list [-h] [--network network]
                           [--output_type json/html/text]

optional arguments:
  -h, --help            show this help message and exit
  --network network, -n network
                        Network to list from (staging, production or both).
                        Default is both
  --output_type json/html/text, -t json/html/text
                        Output type {json, html, text}. Default is text
```

#### List of all policies (default is both networks and text output)
Retrieve a list of all policies in human readable format using a specific instance of the Image Manager behavior available on both networks:

```
$ akamai imaging --section devrel-imaging --policy_set jgarza_sandbox_akamaideveloper_com-10526224 list

Policy: jgarza_sandbox_akamaideveloper_com-10526224 	Network: both 	Output: text

STAGING:
         Policy name |              Date Created |                 User
=============================================================================
               .auto |  2018-04-19 18:18:13+0000 |
                crop |  2018-09-03 17:42:32+0000 |     42uzkarfjv4pzsdf
 jgarza-sandbox-img1 |  2018-04-19 19:50:51+0000 | afdo-worldtour@akamai.com

PRODUCTION:
         Policy name |              Date Created |                 User
=============================================================================
               .auto |  2018-04-19 19:43:05+0000 |               system
                crop |  2018-09-03 17:42:38+0000 |     42uzkarfjv4pzsdf
 jgarza-sandbox-img1 |  2018-04-19 21:11:38+0000 | afdo-worldtour@akamai.com
```

The commands below acomplish the same as the previous one:

```
$ akamai imaging --section devrel-imaging --policy_set jgarza_sandbox_akamaideveloper_com-10526224 list --network both --output_type text

$ akamai imaging --section devrel-imaging --policy_set jgarza_sandbox_akamaideveloper_com-10526224 list -n both -t text
```

#### List policies on the staging network in HTML format 

```
$ akamai imaging --section devrel-imaging --policy_set jgarza_sandbox_akamaideveloper_com-10526224 list --network staging --output_type html
```

#### List policies on the staging network in JSON format 

```
$ akamai imaging --section devrel-imaging --policy_set jgarza_sandbox_akamaideveloper_com-10526224 list --network staging --output_type json
```
Saving the output in JSON format causes all the policies to be merged together on a single JSON response

### Get a policy

#### get Help
```
$ akamai imaging --section devrel-imaging --policy_set jgarza_sandbox_akamaideveloper_com-10526224 get --help 

usage: akamai-imaging get [-h] [--network network] [--output_file file_name]
                          name

positional arguments:
  name                  Policy name to retrieve

optional arguments:
  -h, --help            show this help message and exit
  --network network, -n network
                        Network to list from (staging or production). Default
                        is production
  --output_file file_name, -f file_name
                        Save output to a file
```

#### Get a policy (default is production)

```
$ akamai imaging --section devrel-imaging --policy_set jgarza_sandbox_akamaideveloper_com-10526224 get crop
```

The commands below acomplish the same as the previous one:

```
$ akamai imaging --section devrel-imaging --policy_set jgarza_sandbox_akamaideveloper_com-10526224 get --network production 

$ akamai imaging --section devrel-imaging --policy_set jgarza_sandbox_akamaideveloper_com-10526224 list -n production
```
#### Get the "crop" policy from staging

```
$ akamai imaging --section devrel-imaging --policy_set jgarza_sandbox_akamaideveloper_com-10526224 get crop --network staging 
```

#### Get "crop" policy from staging and save the output to a file called "my_crop_policy.json"

```
$ akamai imaging --section devrel-imaging --policy_set jgarza_sandbox_akamaideveloper_com-10526224 get crop --network staging --output_file my_crop_policy.json 
```

### Set a policy

#### set Help
```
$ akamai imaging --section devrel-imaging --policy_set jgarza_sandbox_akamaideveloper_com-10526224 get --help 

usage: akamai-imaging set [-h] --input_file file_name [--network network] name

positional arguments:
  name                  Policy name to update

optional arguments:
  -h, --help            show this help message and exit
  --input_file file_name, -f file_name
                        JSON Config file
  --network network, -n network
                        Network where the policy resides (staging, production
                        or both). Default is production
```

#### Create (or update) a policy (default is production)

Create a policy called "crop" on production as indicated on a file called my_crop_policy.json
```
$ akamai imaging --section devrel-imaging --policy_set jgarza_sandbox_akamaideveloper_com-10526224 set crop --input_file my_crop_policy.json 
```

The commands below acomplish the same as the previous one:

```
$ akamai imaging --section devrel-imaging --policy_set jgarza_sandbox_akamaideveloper_com-10526224 set crop --input_file my_crop_policy.json --network production

$ akamai imaging --section devrel-imaging --policy_set jgarza_sandbox_akamaideveloper_com-10526224 set crop -f my_crop_policy.json --network production

$ akamai imaging --section devrel-imaging --policy_set jgarza_sandbox_akamaideveloper_com-10526224 set crop -f my_crop_policy.json -n production

```
#### Create (or update) a policy on staging

```
$ akamai imaging --section devrel-imaging --policy_set jgarza_sandbox_akamaideveloper_com-10526224 set crop --input_file my_crop_policy.json --network staging 
```

#### Create (or update) a policy both on staging, and production

```
$ akamai imaging --section devrel-imaging --policy_set jgarza_sandbox_akamaideveloper_com-10526224 set crop --input_file my_crop_policy.json --network both 
```

### Delete a policy

#### delete Help
```
$ akamai imaging --section devrel-imaging --policy_set jgarza_sandbox_akamaideveloper_com-10526224 delete --help 

usage: akamai-imaging delete [-h] [--network network] name

positional arguments:
  name                  Policy name to delete

optional arguments:
  -h, --help            show this help message and exit
  --network network, -n network
                        Network to delete from (staging, production or both).
                        Default is production
```

#### Delete a policy (default is production)

Delete a policy called "crop" on production 
```
$ akamai imaging --section devrel-imaging --policy_set jgarza_sandbox_akamaideveloper_com-10526224 delete crop 
```

The commands below acomplish the same as the previous one:

```
$ akamai imaging --section devrel-imaging --policy_set jgarza_sandbox_akamaideveloper_com-10526224 delete crop --network production

$ akamai imaging --section devrel-imaging --policy_set jgarza_sandbox_akamaideveloper_com-10526224 delete crop -n production

```
#### Delete a policy on staging

Delete a policy called "crop" on staging

```
$ akamai imaging --section devrel-imaging --policy_set jgarza_sandbox_akamaideveloper_com-10526224 delete crop --network staging 
```

#### Delete a policy both on staging, and production

```
$ akamai imaging --section devrel-imaging --policy_set jgarza_sandbox_akamaideveloper_com-10526224 delete crop --network both 
```

## Updating

To update to the latest version:

```
$ akamai update imaging
```
