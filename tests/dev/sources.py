#!/usr/bin/env python3
from pprint import pprint
import os
import sys
import tempfile

from .helpers import err

from ..gpkgs import message as msg
from ..gpkgs import shell_helpers as shell

def test_sources(direpa_src, main_pkg):
   filenpa_pattern=os.path.join(direpa_src, ".refine")
   direpa_dst=os.path.join(tempfile.gettempdir(), "refine-dst")
   if os.path.exists(direpa_dst):
      shell.rmtree(direpa_dst)
   os.makedirs(direpa_dst, exist_ok=True)

   try:
      main_pkg.refine(direpa_src="unknown")
      err()
   except main_pkg.RefineError as e:
      if not "directory not found" in str(e):
         raise

   try:
      main_pkg.refine(direpa_src=direpa_src, filenpa_patterns=3)
      err()
   except main_pkg.RefineError as e:
      if not "option filenpa_patterns must be of type" in str(e):
         raise

   try:
      main_pkg.refine(direpa_src=direpa_src, filenpa_patterns=[direpa_dst])
      err()
   except main_pkg.RefineError as e:
      if not "filenpa_patterns path is not a file" in str(e):
         raise

   try:
      main_pkg.refine(direpa_src=direpa_src, filenpa_patterns=["unknown.txt"])
      err()
   except main_pkg.RefineError as e:
      if not "filenpa_patterns path not found" in str(e):
         raise

   output_paths=main_pkg.refine(
      direpa_src, 
      patterns=[], 
      get_abs_paths=False,
      keep_empty_dir=True,
      filenpa_patterns=[filenpa_pattern],
      direpa_dst=direpa_dst,
   )

   pprint(output_paths)

   msg.success("Passed sources test from {} to {}".format(direpa_src, direpa_dst))