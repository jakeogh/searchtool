#!/usr/bin/env python3
# -*- coding: utf8 -*-
# tab-width:4

# pylint: disable=C0111  # docstrings are always outdated and wrong
# pylint: disable=C0114  # Missing module docstring (missing-module-docstring)
# pylint: disable=W0511  # todo is encouraged
# pylint: disable=C0301  # line too long
# pylint: disable=R0902  # too many instance attributes
# pylint: disable=C0302  # too many lines in module
# pylint: disable=C0103  # single letter var names, func name too descriptive
# pylint: disable=R0911  # too many return statements
# pylint: disable=R0912  # too many branches
# pylint: disable=R0915  # too many statements
# pylint: disable=R0913  # too many arguments
# pylint: disable=R1702  # too many nested blocks
# pylint: disable=R0914  # too many local variables
# pylint: disable=R0903  # too few public methods
# pylint: disable=E1101  # no member for base
# pylint: disable=W0201  # attribute defined outside __init__
# pylint: disable=R0916  # Too many boolean expressions in if statement
# pylint: disable=C0305  # Trailing newlines editor should fix automatically, pointless warning

import asyncio
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal
from typing import Sequence
from typing import Union

import click
from asserttool import ic
from click_auto_help import AHGroup
from clicktool import click_add_options
from clicktool import click_global_options
from clicktool import tv
from mptool import output
from mptool import unmp
from youtubesearchpython.__future__ import VideosSearch

signal(SIGPIPE, SIG_DFL)


def print_result(
    *,
    result,
    term: str,
    tty: bool,
    dict_input: bool,
    verbose: Union[bool, int, float],
):
    results = result["result"]
    # ic(type(results))
    # ic(len(results))
    for _result in results:
        # ic(_result["link"], _result["title"])
        out_dict = {_result["title"]: _result["link"]}
        output(out_dict, reason=term, dict_input=dict_input, tty=tty, verbose=verbose)


async def main(
    *, term: str, tty: bool, dict_input: bool, verbose: Union[bool, int, float]
):
    search = VideosSearch(term)
    while True:
        result = await search.next()
        print_result(
            result=result, term=term, tty=tty, dict_input=dict_input, verbose=verbose
        )

    # result = await search.next()
    # print_result(result)


@click.group(no_args_is_help=True, cls=AHGroup)
@click_add_options(click_global_options)
@click.pass_context
def cli(
    ctx,
    verbose: Union[bool, int, float],
    verbose_inf: bool,
    dict_input: bool,
) -> None:

    tty, verbose = tv(
        ctx=ctx,
        verbose=verbose,
        verbose_inf=verbose_inf,
    )


@cli.command("youtube")
@click.argument("terms", type=str, nargs=-1)
@click_add_options(click_global_options)
@click.pass_context
def _youtube(
    ctx,
    terms: Sequence[str],
    verbose: Union[bool, int, float],
    verbose_inf: bool,
    dict_input: bool,
) -> None:

    tty, verbose = tv(
        ctx=ctx,
        verbose=verbose,
        verbose_inf=verbose_inf,
    )

    if terms:
        iterator = terms
    else:
        iterator = unmp(
            valid_types=[
                str,
            ],
            verbose=verbose,
        )
    del terms

    index = 0
    for index, _term in enumerate(iterator):
        if verbose:
            ic(index, _term)

        asyncio.run(main(term=_term, tty=tty, dict_input=dict_input, verbose=verbose))


if __name__ == "__main__":
    # pylint: disable=E1120
    cli()
