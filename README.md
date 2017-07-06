# Akamai CLI: Image Manager Module

This module enables the use of Image Manager in the Akamai CLI tool

## Install

Installation is done via `akamai get`:

```
$ akamai get brassic-lint/cli-imgman
```


## Usage

```
usage: akamai imgman [-h] [--verbose] [--debug] [--edgerc CONFIG_FILE]
                     [--section CONFIG_SECTION]
                     [--output_file OUTPUT_FILE] --policy_set POLICY_SET
                     {list,retrieve,add,update,delete} ...

Process command line options.

positional arguments:
  {list,retrieve,add,update,delete}
                        commands
    list                Subcommands
    retrieve            Retrieve policy
    add                 Add policy
    update              Update policy
    delete              Delete policy

optional arguments:
  -h, --help            show this help message and exit
  --verbose, -v
  --debug, -d
  --edgerc CONFIG_FILE, -e CONFIG_FILE
  --section CONFIG_SECTION, -s CONFIG_SECTION
  --output_file OUTPUT_FILE, -f OUTPUT_FILE   Output file {list, retrieve}

Required arguments:
  --policy_set POLICY_SET, -p POLICY_SET
```

## Updating

To update to the latest version:

```
$ akamai update imgman
```
