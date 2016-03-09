# mtg_ssm - Magic: the Gathering Spreadsheet Manager

[![Build Status](https://travis-ci.org/gwax/mtg_ssm.svg?branch=master)](https://travis-ci.org/gwax/mtg_ssm)
[![Coverage Status](https://coveralls.io/repos/github/gwax/mtg_ssm/badge.svg?branch=master)](https://coveralls.io/github/gwax/mtg_ssm?branch=master)

This is a tool for creating/updating user-friendly spreadsheets with
Magic: the Gathering collection information. The tool can also import/export
data to/from these spreadsheets to other formats, such as CSV files.

As a matter of convenience, you can store the created spreadsheet in
Dropbox, Google Drive, or the like and access your collection from
anywhere.


# Installation

mtg_ssm is available on PyPI so, if you have python (>=3.4) and pip installed
on your system, you should be able to get mtg_ssm by entering the following
into a terminal:

```bash
pip3 install mtg_ssm
```

Updates can be performed by entering:

```bash
pip3 install -U mtg_ssm
```

You can verify installation from the terminal by running:

```bash
mtg-ssm --help
```


# Usage

For first time use, you will want to create an empty spreadsheet with card data:

```bash
mtg-ssm collection.xlsx
```

In the future, when new sets are released, running the same command will update
your collection spreadsheet while keeping existing counts:

```bash
mtg-ssm collection.xlsx
```

## Existing collections

If you already have your cards in another collection store, you might want to
import that collection into your card spreadsheet.

First create an example csv file:

```bash
mtg-ssm --format csv collection.csv.example
```

Then modify the template to match your counts and import into your spreadsheet:

```bash
mtg-ssm collection.xlsx collection.csv
```


# Contributions

Pull requests are welcome and contributions are greatly appreciated.

Issues can be reported via GitHub.


# Acknowledgments

* [Wizards of the Coast](http://magic.wizards.com/): For making Magic: the
Gathering and continuing to support it. Off and on, it's been my favorite
hobby since the early '90s.
* [MTG JSON](http://mtgjson.com): MTG JSON is an amazing resource
for anyone looking to build tools around magic card data. It is pretty much
**THE** source for structured magic card data. Without MTG JSON this
project would not have been possible.


# Changelog



## 1.2.0

* Complete rework of the serialization architecture.
* Rebuild of the manager cli.
* CLI interface changes. See help for changes.

## 1.1.0

* Complete rework of the data model storage. Drop sqlite based data models in favor of custom classes and dict based indexes.

## 1.0.2

* Version bump MTGJSON support.

## 1.0.1

* Fixed some PyPI related issues.

## 1.0.0

* Initial stable release.
