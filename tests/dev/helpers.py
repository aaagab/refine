#!/usr/bin/env python3
from pprint import pprint
import inspect
from inspect import currentframe, getframeinfo
import os
import sys
import time

from ..gpkgs import message as msg

def err():
    direpa_script=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    frameinfo = getframeinfo(currentframe().f_back)
    filenpa=os.path.relpath(frameinfo.filename, direpa_script)
    text="At '{}' line '{}' test failed.".format(filenpa, frameinfo.lineno)
    msg.error(text, trace=True, exit=1)



