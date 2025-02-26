#!/usr/bin/env python3
import os
direpa_script=os.path.dirname(os.path.realpath(__file__))

from .dev.refine import refine, PathElem as _PathElem
from .dev.patterns import Pattern as _Pattern, set_pattern as _set_pattern
from .dev.exceptions import RefineError, RefinePatternError

if os.path.exists(os.path.join(direpa_script, "tests")):
    from .tests.dev.patterns import test_patterns as _test_patterns
    from .tests.dev.path_elems import test_path_elems as _test_path_elems
    from .tests.dev.refine import test_refine as _test_refine
    from .tests.dev.sources import test_sources as _test_sources