#!/usr/bin/env python3
import os
from pprint import pprint
import glob
import re

if __name__ == "__main__":
    import sys, os
    import importlib
    direpa_src=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    direpa_script_parent=os.path.dirname(direpa_src)
    module_name=os.path.basename(direpa_src)
    sys.path.insert(0, direpa_script_parent)
    main_pkg = importlib.import_module(module_name)
    del sys.path[0]

    direpa_test=os.path.join(direpa_src, "tests")
    module_name=os.path.basename(direpa_test)
    sys.path.insert(0, direpa_src)
    test_pkg = importlib.import_module(module_name)
    del sys.path[0]

    test_pkg.test_patterns(main_pkg)
    test_pkg.test_path_elems(direpa_test, main_pkg)
    test_pkg.test_refine(direpa_test, main_pkg)
    test_pkg.test_sources(direpa_src, main_pkg)
