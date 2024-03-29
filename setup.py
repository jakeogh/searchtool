# -*- coding: utf-8 -*-


from setuptools import find_packages
from setuptools import setup

import fastentrypoints

dependencies = ["click"]

config = {
    "version": "0.1",
    "name": "searchtool",
    "url": "https://github.com/jakeogh/searchtool",
    "license": "ISC",
    "author": "Justin Keogh",
    "author_email": "github.com@v6y.net",
    "description": "common search engine functions",
    "long_description": __doc__,
    "packages": find_packages(exclude=["tests"]),
    "package_data": {"searchtool": ["py.typed"]},
    "include_package_data": True,
    "zip_safe": False,
    "platforms": "any",
    "install_requires": dependencies,
    "entry_points": {
        "console_scripts": [
            "searchtool=searchtool.searchtool:cli",
        ],
    },
}

setup(**config)
