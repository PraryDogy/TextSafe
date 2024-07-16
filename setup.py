# -*- coding: utf-8 -*-

"""
    python setup.py py2app
"""

import shutil
import sys
import traceback
from datetime import datetime

from setuptools import setup

from cfg import Cfg
from setup_ext import SetupExt

current_year = datetime.now().year

APP = ["start.py"]

DATA_FILES = [
    "icon.icns",
    "icon.png"
    ]

OPTIONS = {"iconfile": "icon.icns",
           "plist": {"CFBundleName": Cfg.app_name,
                     "CFBundleShortVersionString": Cfg.app_ver,
                     "CFBundleVersion": Cfg.app_ver,
                     "CFBundleIdentifier": f"com.evlosh.{Cfg.app_name}",
                     "NSHumanReadableCopyright": (
                         f"Created by Evgeny Loshkarev"
                         f"\nCopyright © {current_year} MIUZ Diamonds."
                         f"\nAll rights reserved.")}}


if __name__ == "__main__":
    sys.argv.append("py2app")

    try:
        setup(
            app=APP,
            name=Cfg.app_name,
            data_files=DATA_FILES,
            options={"py2app": OPTIONS},
            setup_requires=["py2app"],
            )
        SetupExt(appname=Cfg.app_name)

    except Exception:
        print(traceback.format_exc())

        try:
            shutil.rmtree("build")
            shutil.rmtree(".eggs")
            shutil.rmtree("dist")
        except FileNotFoundError:
            pass
