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
- `--output_file OUTPUT_FILE`, `-f OUTPUT_FILE` - Output file {list, retrieve}
- `--verbose` - Print verbose information
- `--version`, `-v` — Print the version
- `--help`, `-h` — Show help

## Commands  
- `add` - Add a policy
- `delete` - Delete a policy
- `list` — List policies
- `retrieve` — Retrieve a specific policy
- `update` — Update policy


Required arguments:
  --policy_set POLICY_SET, -p POLICY_SET
```

## Examples

Retrieve a list of all policies using a specific instance of the Image Manager behavior:

```
$ akamai imaging --section devrel-imaging -p jgarza_sandbox_akamaideveloper_com-10526224 list
```

## Updating

To update to the latest version:

```
$ akamai update imaging
```
