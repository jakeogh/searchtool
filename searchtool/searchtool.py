#!/usr/bin/env python3
# -*- coding: utf8 -*-
# tab-width:4

# pylint: disable=missing-docstring               # [C0111] docstrings are always outdated and wrong
# pylint: disable=missing-module-docstring        # [C0114]
# pylint: disable=fixme                           # [W0511] todo is encouraged
# pylint: disable=line-too-long                   # [C0301]
# pylint: disable=too-many-instance-attributes    # [R0902]
# pylint: disable=too-many-lines                  # [C0302] too many lines in module
# pylint: disable=invalid-name                    # [C0103] single letter var names, name too descriptive
# pylint: disable=too-many-return-statements      # [R0911]
# pylint: disable=too-many-branches               # [R0912]
# pylint: disable=too-many-statements             # [R0915]
# pylint: disable=too-many-arguments              # [R0913]
# pylint: disable=too-many-nested-blocks          # [R1702]
# pylint: disable=too-many-locals                 # [R0914]
# pylint: disable=too-few-public-methods          # [R0903]
# pylint: disable=no-member                       # [E1101] no member for base
# pylint: disable=attribute-defined-outside-init  # [W0201]
# pylint: disable=too-many-boolean-expressions    # [R0916] in if statement

from __future__ import annotations

import asyncio
import sys
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal

import click
from asserttool import ic
from click_auto_help import AHGroup
from clicktool import click_add_options
from clicktool import click_global_options
from clicktool import tv
from mptool import output
from unmp import unmp
from youtubesearchpython.__future__ import VideosSearch

signal(SIGPIPE, SIG_DFL)


def print_result(
    *,
    result,
    term: str,
    tty: bool,
    dict_output: bool,
    verbose: bool | int | float = False,
):
    results = result["result"]
    # ic(type(results))
    # ic(len(results))
    for _result in results:
        # ic(_result["link"], _result["title"])
        out_dict = {_result["title"]: _result["link"]}
        output(
            out_dict,
            reason=term,
            dict_output=dict_output,
            tty=tty,
            flush=True,
        )


async def main(
    *,
    term: str,
    tty: bool,
    dict_output: bool,
    verbose: bool | int | float = False,
):
    search = VideosSearch(term)
    while True:
        try:
            result = await search.next()
        except Exception as e:
            ic(e)
            # raise Exception('ERROR: Could not parse YouTube response.')
            if (
                e.args[0] == "ERROR: Could not parse YouTube response."
            ):  # no more results
                sys.exit(0)

        print_result(
            result=result,
            term=term,
            tty=tty,
            dict_output=dict_output,
        )

    # result = await search.next()
    # print_result(result)


@click.group(no_args_is_help=True, cls=AHGroup)
@click_add_options(click_global_options)
@click.pass_context
def cli(
    ctx,
    verbose_inf: bool,
    dict_output: bool,
    verbose: bool | int | float = False,
) -> None:
    tty, verbose = tv(
        ctx=ctx,
        verbose=verbose,
        verbose_inf=verbose_inf,
    )
    if not verbose:
        ic.disable()


@cli.command("youtube")
@click.argument("terms", type=str, nargs=-1)
@click_add_options(click_global_options)
@click.pass_context
def _youtube(
    ctx,
    terms: tuple[str, ...],
    verbose_inf: bool,
    dict_output: bool,
    verbose: bool | int | float = False,
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
        )
    del terms

    index = 0
    for index, _term in enumerate(iterator):
        ic(index, _term)
        asyncio.run(main(term=_term, tty=tty, dict_output=dict_output))
