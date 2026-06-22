#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

def resource_path(relative_path: str) -> str:
    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.getcwd()

    return os.path.join(base_path, relative_path)
