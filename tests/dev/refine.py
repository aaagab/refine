#!/usr/bin/env python3
from pprint import pprint
import os
import sys
import tempfile

from .helpers import err
from .refine_paths import get_refine_paths

from ...dev.refine import refine

from ...gpkgs import message as msg
from ...gpkgs import shell_helpers as shell


def test_refine():
   direpa_src=os.path.join(tempfile.gettempdir(), "refine-src")
   direpa_refine=os.path.join(tempfile.gettempdir(), "refine")
   filenpa_pattern=os.path.join(direpa_refine, ".refine")
   direpa_dst=os.path.join(tempfile.gettempdir(), "refine-dst")
   _index=None
   # _index=31
   # _index="last"
   _refines, max_index=get_refine_paths(direpa_src, direpa_dst, index=_index)

   if _index == "last":
      _index=max_index
   index=0
   for dy_ref in _refines:
      for _path in [
         direpa_refine,
         direpa_src,
         direpa_dst,
      ]:
         if os.path.exists(_path):
            shell.rmtree(_path)
         os.makedirs(_path, exist_ok=True)

      for _path in dy_ref["paths"]:
         _path_elem=os.path.join(direpa_src, _path)
         if _path[-1] == "/":
            os.makedirs(_path_elem, exist_ok=True)
         else:
            basename=os.path.basename(_path_elem)
            if basename != _path_elem:
               direpa_elem=_path_elem[:-len(basename)]
               os.makedirs(direpa_elem, exist_ok=True)
            open(_path_elem, "w").close()

      _patterns=dy_ref["patterns"]
      filenpa_patterns=[]
      if dy_ref["test_filenpa_patterns"] is True:
         with open(filenpa_pattern, "w") as f:
            for pattern in dy_ref["patterns"]:
               f.write("{}\n".format(pattern))
         filenpa_patterns.append(filenpa_pattern)
         dy_ref["patterns"]=[]

      _direpa_dst=None
      if dy_ref["test_direpa_dst"] is True:
         _direpa_dst=direpa_dst

      print_index=None
      if _index is None:
         print_index=index
      else:
         print_index=_index


      output_paths=refine(
         direpa_src, 
         patterns=dy_ref["patterns"], 
         get_abs_paths=dy_ref["get_abs_paths"],
         keep_empty_dir=dy_ref["keep_empty_dir"],
         filenpa_patterns=filenpa_patterns,
         direpa_dst=_direpa_dst,
      )

      if dy_ref["test_direpa_dst"] is True:
         output_paths=get_paths(
            direpa_dst=direpa_dst,
            get_abs_paths=dy_ref["get_abs_paths"],
            keep_empty_dir=dy_ref["keep_empty_dir"],
         )

      test_paths(
         dy_ref,
         output_paths,
         print_index,
         _patterns,
         direpa_src,
         direpa_dst,
         dy_ref["get_abs_paths"],
         dy_ref["test_direpa_dst"],
      )

      msg.success("{}/{} Passed refine '{}'".format(print_index, max_index, _patterns))
      index+=1

def get_paths(
   direpa_dst,
   get_abs_paths,
   keep_empty_dir,
   _paths=None,
   _is_root=True,
   _direpa_parent=None,
   _direpa_path=None,
):
   if _paths is None:
      _paths=[]
      _direpa_parent=direpa_dst

   elems=os.listdir(direpa_dst)

   if _direpa_path is not None:
      if keep_empty_dir is True:
         _paths.append(_direpa_path)
      else:
         if len(elems) > 0:
            _paths.append(_direpa_path)

   for elem in sorted(elems):
      _direpa_path=None
      path_elem=os.path.join(direpa_dst, elem)
      _path=None
      if get_abs_paths is True:
         _path=path_elem
      else:
         _path=os.path.relpath(path_elem, _direpa_parent)

      if os.path.isdir(path_elem):
         _direpa_path=_path
         get_paths(
            direpa_dst=path_elem,
            get_abs_paths=get_abs_paths,
            keep_empty_dir=keep_empty_dir,
            _paths=_paths,
            _is_root=False,
            _direpa_parent=_direpa_parent,
            _direpa_path=_direpa_path,
         )
      else:
         _paths.append(_path)

   if _is_root is True:
      return _paths

def test_paths(
   dy_ref, 
   output_paths, 
   print_index, 
   patterns,
   direpa_src, 
   direpa_dst,
   get_abs_paths,
   test_direpa_dst,
):
   for attr in ["discarded", "not_discarded"]:
      if attr in dy_ref:
         for _path in dy_ref[attr]:
            check_path=None
            if get_abs_paths is True:
               if test_direpa_dst is True:
                  rel_path=os.path.relpath(_path, direpa_dst)
                  check_path=os.path.join(direpa_src, rel_path)
               else:
                  check_path=_path
            else:
               check_path=os.path.join(direpa_src, _path)

            error=None
            if os.path.exists(check_path):
               if attr == "discarded":
                  if _path in output_paths:
                     error="For attribute '{}' ERROR NOT expected path '{}' FOUND in output_paths.".format( attr, _path)
               else:
                  if _path not in output_paths:
                     error="For attribute '{}' ERROR expected path '{}' NOT FOUND in output_paths".format( attr, _path)
            else:
               error="For attribute '{}' ERROR test path NOT FOUND '{}' in direpa_src".format( attr, _path)

            if error is not None:
               print()
               print("index: {}".format(print_index))

               print()
               print("paths:")
               pprint(dy_ref["paths"])
               
               print()
               print("patterns:")
               pprint(patterns)

               print()
               print("{}:".format(attr))
               pprint(dy_ref[attr])

               print()
               if test_direpa_dst is True:
                  print("output_paths (from dst '{}'):".format(direpa_dst))
               else:
                  print("output_paths (from refine):")
               pprint(output_paths)

               print()
               msg.warning(error)

               print()
               err()
