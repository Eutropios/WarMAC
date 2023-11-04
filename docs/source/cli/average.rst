.. _average:

#########
 Average
#########

|  The Average command can be used to find the average platinum price of a
   particular item.

USE PIP DOCUMENTATION AS A GUIDE FOR MULTI-SUBCOMMAND DOCS

.. code:: console

   usage: warmac average [-s <stat>] [-p <platform>] [-t <days>] [-m | -r] [-b] item

   Calculate the average platinum price of an item. Able to find the median, mean, mode,
   geometric mean, and harmonic mean of the specified item.

   positional arguments:
   item                       Item to find the statistic of. If the item spans multiple words,
                              please enclose the item within quotation marks.

   options:
   -s, --stats <stat>         Specifies which statistic to return; Can be one of [median, mean, mode, harmonic, geometric]. (Default: median)
   -p, --platform <platform>  Specifies which platform to fetch orders for; Can be one of [pc, ps4, xbox, switch]. (Default: pc)
   -t, --timerange <days>     Specifies in days how old the orders can be. Must be in range [1, 60]. (Default: 10)
   -m, --maxrank              Get price statistic of the mod/arcane at max rank instead of at unranked. (Default: False)
   -r, --radiant              Get price statistic of the relic at radiant refinement instead of at intact. (Default: False)
   -b, --buyers               Take the average platinum price from buyer orders instead of from seller orders. (Default: False)
   -v, --verbose              Prints additional information about the program.
   -h, --help                 Show this message and exit.

THIS IS ALL BLACK STUFF, IT'S JUST HERE FOR REFERENCE

## Usage

To get started right away with sensible defaults:

```sh black {source_file_or_directory} ```

You can run _Black_ as a package if running it as a script doesn't work:

```sh python -m black {source_file_or_directory} ```

### Command line options

The CLI options of _Black_ can be displayed by running `black --help`. All
options are also covered in more detail below.

While _Black_ has quite a few knobs these days, it is still opinionated so style
options are deliberately limited and rarely added.

Note that all command-line options listed above can also be configured using a
`pyproject.toml` file (more on that below).

#### `-c`, `--code`

Format the code passed in as a string.

```console $ black --code "print ( 'hello, world' )" print("hello, world") ```

#### `-l`, `--line-length`

How many characters per line to allow. The default is 88.

See also [the style documentation](labels/line-length).
