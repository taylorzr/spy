# Spy

![Spy vs Spy](spy.jpg "spy")

## Configuration

`cp .envrc.sample .envrc`, set your org, and `direnv allow`

## Usage

There is a makefile. Default make will run setup and one iteration. On first run, db will be initialized, no diffs are recorded. Subsequent runs will record set differences, and individual differences, and printed to stdout.

TODO: Add examples of set and individual changes

## Todo

* roadmap
  * supporting re-added users, but that get's recorded under user changes not set changes
  * other outputs
    * signal? or discord?
    * whatever anyone wants, plugin system or something
  * other attrs
    * repo creation
    * follow/ing/ers

## sqlite basics

```sqlite
sqlite3 spy.db
sqlite> .tables
sqlite> .schema users
```
