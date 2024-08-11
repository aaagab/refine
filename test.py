#!/usr/bin/env python3
import os
import sys
import importlib

if __name__ == "__main__":
    direpa_script=os.path.dirname(os.path.realpath(__file__))
    direpa_script_parent=os.path.dirname(direpa_script)
    module_name=os.path.basename(os.path.dirname(os.path.realpath(__file__)))
    sys.path.insert(0, direpa_script_parent)
    pkg = importlib.import_module(module_name)
    del sys.path[0]

    pkg._test_patterns()
    pkg._test_path_elems()
    pkg._test_refine()
    pkg._test_sources(direpa_script)
