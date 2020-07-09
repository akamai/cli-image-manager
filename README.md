<!--esi 
<esi:assign name="dac_stylesheets" value="['/stylesheets/screen.css']" />
<esi:assign name="dac_footer_js" value="['/javascripts/app/toc.js']" />
<esi:eval src="/internal/header.html?http" dca="esi" />
-->
# Akamai CLI: Image and Video Manager Module

This module enables the use of Image and Video Manager (IM) in the Akamai CLI tool

## API Permissions

Please ensure your API client has access to the "Image Manager" API (you may need to create a separate API client)

## Install

To install, use [Akamai CLI](https://github.com/akamai/cli):

```
akamai install image-manager
```

You may also use this as a stand-alone command by cloning this repository
and compiling it yourself.

## Usage

```
akamai image-manager [global flags] --policy-set POLICY-SET command
```

## Global Flags
- `--edgerc value` — Location of the credentials file (default: user's directory like "/Users/jgarza") [$AKAMAI_EDGERC]
- `--section value` — Section of the credentials file (default: "default") [$AKAMAI_EDGERC_SECTION]
- `--debug` - `-d` - prints debug information
- `--verbose` - Print verbose information
- `--version`, `-v` — Print the version
- `--policy-set POLICY-SET` (REQUIRED) Name of the Image Manager policy to manage (grep for "policyTokenDefault" within the Property Manager configuration)
- `--help`, `-h` — Show help

## Commands  
- `list-policies` — List existing policies on given network, or both (default). Output can be formatted as JSON, or text tables (default); which is a human readable ascii table showing the policy name, creation date and creation user (useful for inventorying purposes).
- `get-policy` — Retrieves a given policy on a given network (output can be saved into a file)
- `set-policy` - Creates or updates a given policy on a given network (or both) using the JSON provided on a given input file
- `delete-policy` - Deletes a policy (given network or both)

Required arguments:
  --policy-set POLICY-SET, -p POLICY-SET

## Examples

### Listing

#### list Help

Showing the syntax
```
$ akamai image-manager --section default --policy-set example_com list-policies --help

usage: akamai-image-manager list-policies [-h] [--network network]
                           [--output-type json/text]

optional arguments:
  -h, --help            show this help message and exit
  --network network, -n network
                        Network to list from (staging, production or both).
                        Default is both
  --output-type json/text, -t json/text
                        Output type {json, text}. Default is text
```

#### List of all policies (default is both networks and text output)
Retrieve a list of all policies in human readable format using a specific instance of the Image Manager behavior available on both networks:

```
$ akamai image-manager --section default --policy-set example_com list-policies

Policy: example_com 	Network: both 	Output: text

STAGING:
+--------------------------------+---------------------------+---------------------------+
|          Policy name           |       Date Created        |           User            |
+================================+===========================+===========================+
|             .auto              | 2018-04-19 18:18:13+0000  |          system           |
+--------------------------------+---------------------------+---------------------------+
|           HeroBanner           | 2018-09-03 17:42:32+0000  |     42uzkarfjv4pzsdf      |
+--------------------------------+---------------------------+---------------------------+
|         AvatarThumbnail        | 2018-04-19 19:50:51+0000  |     42uzkarfjv4pzsdf      |
+--------------------------------+---------------------------+---------------------------+

PRODUCTION:
+--------------------------------+---------------------------+---------------------------+
|          Policy name           |       Date Created        |           User            |
+================================+===========================+===========================+
|             .auto              | 2018-04-19 19:43:05+0000  |          system           |
+--------------------------------+---------------------------+---------------------------+
|           HeroBanner           | 2018-09-03 17:42:38+0000  |     42uzkarfjv4pzsdf      |
+--------------------------------+---------------------------+---------------------------+
|         AvatarThumbnail        | 2018-04-19 21:11:38+0000  |     42uzkarfjv4pzsdf      |
+--------------------------------+---------------------------+---------------------------+
```

The commands below accomplish the same as the previous one:

```
$ akamai image-manager --section default --policy-set example_com list-policies --network both --output-type text

$ akamai image-manager --section default --policy-set example_com list-policies -n both -t text
```

#### List policies on the staging network in JSON format

```
$ akamai image-manager --section default --policy-set example_com list-policies --network staging --output-type json
```
Saving the output in JSON format causes all the policies to be merged together on a single JSON response

### Get a policy

#### get-policy Help
```
$ akamai image-manager --section default --policy-set example_com get-policy --help

usage: akamai-image-manager get-policy [-h] [--network network] [--output-file filename]
                          name

positional arguments:
  name                  Policy name to retrieve

optional arguments:
  -h, --help            show this help message and exit
  --network network, -n network
                        Network to list from (staging or production). Default
                        is production
  --output-file filename, -f filename
                        Save output to a file
```

#### Get the "HeroBanner" policy (default is production)

```
$ akamai image-manager --section default --policy-set example_com get-policy HeroBanner
```

The commands below accomplish the same as the previous one:

```
$ akamai image-manager --section default --policy-set example_com get-policy HeroBanner --network production

$ akamai image-manager --section default --policy-set example_com get-policy HeroBanner -n production
```
#### Get the "HeroBanner" policy from staging

```
$ akamai image-manager --section default --policy-set example_com get-policy HeroBanner --network staging
```

#### Get "HeroBanner" policy from staging and save the output to a file called "rules.json"

```
$ akamai image-manager --section default --policy-set example_com get-policy HeroBanner --network staging --output-file rules.json
```

### Set a policy

#### set-policy Help
```
$ akamai image-manager --section default --policy-set example_com set-policy --help

usage: akamai-image-manager set-policy [-h] --input-file filename [--network network] name

positional arguments:
  name                  Policy name to update

optional arguments:
  -h, --help            show this help message and exit
  --input-file filename, -f filename
                        JSON Config file
  --network network, -n network
                        Network where the policy resides (staging, production
                        or both). Default is production
```

#### Create (or update) a policy (default is production)

Create a policy called "HeroBanner" on production as indicated on a file called rules.json
```
$ akamai image-manager --section default --policy-set example_com set-policy HeroBanner --input-file rules.json
```

The commands below accomplish the same as the previous one:

```
$ akamai image-manager --section default --policy-set example_com set-policy HeroBanner --input-file rules.json --network production

$ akamai image-manager --section default --policy-set example_com set-policy HeroBanner -f rules.json --network production

$ akamai image-manager --section default --policy-set example_com set-policy HeroBanner -f rules.json -n production

```
#### Create (or update) a policy on staging

```
$ akamai image-manager --section default --policy-set example_com set-policy HeroBanner --input-file rules.json --network staging
```

#### Create (or update) a policy both on staging, and production

```
$ akamai image-manager --section default --policy-set example_com set-policy HeroBanner --input-file rules.json --network both
```

### Delete a policy

#### delete Help
```
$ akamai image-manager --section default --policy-set example_com delete-policy --help

usage: akamai-image-manager delete-policy [-h] [--network network] name

positional arguments:
  name                  Policy name to delete

optional arguments:
  -h, --help            show this help message and exit
  --network network, -n network
                        Network to delete from (staging, production or both).
                        Default is production
```

#### Delete a policy (default is production)

Delete a policy called "HeroBanner" on production
```
$ akamai image-manager --section default --policy-set example_com delete-policy HeroBanner
```

The commands below accomplish the same as the previous one:

```
$ akamai image-manager --section default --policy-set example_com delete-policy HeroBanner --network production

$ akamai image-manager --section default --policy-set example_com delete-policy HeroBanner -n production

```
#### Delete a policy on staging

Delete a policy called "HeroBanner" on staging

```
$ akamai image-manager --section default --policy-set example_com delete-policy HeroBanner --network staging
```

#### Delete a policy both on staging, and production

```
$ akamai image-manager --section default --policy-set example_com delete-policy HeroBanner --network both
```

## Updating

To update to the latest version:

```
$ akamai update image-manager
```

## Bugs / Enhancement requests

Please report any issues or enhancement ideas [here in GitHub](https://github.com/akamai/cli-image-manager/issues). Pull requests are welcomed!

## Installation issues

TBD
<!--esi 
<esi:eval src="/internal/footer.html?http" dca="esi" />
-->
