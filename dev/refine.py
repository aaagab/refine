#!/usr/bin/env python3
import os
from pprint import pprint
import re
import shutil
import sys

from .exceptions import RefineError
from .patterns import get_path_level, Pattern, set_pattern

def refine(
	direpa_src, 
	patterns=None, 
	get_abs_paths=True,
	filenpa_patterns=None,
	direpa_dst=None,
	keep_empty_dir=True,
):
	if patterns is None:
		patterns=[]

	tmp_patterns=[]

	if not os.path.exists(direpa_src):
		raise RefineError("For option direpa_src directory not found '{}'.".format(direpa_src))

	if direpa_dst is not None:
		os.makedirs(direpa_dst, exist_ok=True)

	if filenpa_patterns is not None:
		if not isinstance(filenpa_patterns, list):
			raise RefineError("option filenpa_patterns must be of type {}.".format(list))

		for filenpa_pattern in filenpa_patterns:
			if not os.path.isabs(filenpa_pattern):
				filenpa_pattern=os.path.join(direpa_src, filenpa_pattern)

			filenpa_pattern=os.path.normpath(filenpa_pattern)

			if not os.path.exists(filenpa_pattern):
				raise RefineError("For option filenpa_patterns path not found '{}'.".format(filenpa_pattern))

			if not os.path.isfile(filenpa_pattern):
				raise RefineError("For option filenpa_patterns path is not a file '{}'.".format(filenpa_pattern))

			with open(filenpa_pattern, "r") as f:
				lines=f.read().splitlines()
				for line in lines:
					pattern_text=set_pattern(line)
					if pattern_text is not None:
						tmp_patterns.append(Pattern(pattern_text))

	for pattern in patterns:
		pattern_text=set_pattern(pattern)
		if pattern_text is not None:
			tmp_patterns.append(Pattern(pattern_text))

	patterns=tmp_patterns

	refined_paths=process_tree(
		direpa_src, 
		patterns,
		get_abs_paths=get_abs_paths,
		keep_empty_dir=keep_empty_dir,
		direpa_dst=direpa_dst,
	)

	return refined_paths

def process_tree(
	direpa_src, 
	patterns,
	get_abs_paths,
	keep_empty_dir,
	direpa_dst=None,
	_path_elems=None, 
	_direpa_root=None,
	_parent_path_elem=None,
	_make_dir_dst=None,
	_dir_path_elem=None,
):
	is_root=False
	if _path_elems is None:
		is_root=True
		_path_elems=[]
		_direpa_root=direpa_src

	elems=os.listdir(direpa_src)

	if _dir_path_elem is not None:
		if keep_empty_dir is True:
			_path_elems.append(_dir_path_elem)
		else:
			if len(elems) > 0:
				_path_elems.append(_dir_path_elem)

	if _make_dir_dst is not None:
		if keep_empty_dir is True:
			os.makedirs(_make_dir_dst, exist_ok=True)
		else:
			if len(elems) > 0:
				os.makedirs(_make_dir_dst, exist_ok=True)

	for elem in sorted(elems):
		_dir_path_elem=None
		_make_dir_dst=None
		_path_elem=os.path.join(direpa_src, elem).replace("\\", "/")
		isdir=os.path.isdir(_path_elem)
		if isdir is True:
			isfile=False
		else:
			isfile=os.path.isfile(_path_elem)

		if isdir or isfile:
			path_elem=PathElem(
				elem,
				_path_elem, 
				_direpa_root,
				isfile,
				patterns,
				parent=_parent_path_elem,
			)

			if path_elem.is_discarded is False:
				tmp_path_elem=None
				if get_abs_paths is True:
					tmp_path_elem=path_elem.path_elem
				else:
					tmp_path_elem=path_elem.path_text

				path_dst=None
				if direpa_dst is not None:
					path_dst=os.path.join(direpa_dst, path_elem.path_text)

				if path_elem.isfile is True:
					_path_elems.append(tmp_path_elem)
					if path_dst is not None:
						shutil.copy2(path_elem.path_elem, path_dst)
				else:
					_dir_path_elem=tmp_path_elem
					if path_dst is not None:
						_make_dir_dst=path_dst

			if path_elem.is_recursive:
				process_tree(
					path_elem.path_elem, 
					patterns, 
					get_abs_paths=get_abs_paths,
					keep_empty_dir=keep_empty_dir,
					direpa_dst=direpa_dst,
					_path_elems=_path_elems,
					_direpa_root=_direpa_root,
					_parent_path_elem=path_elem,
					_make_dir_dst=_make_dir_dst,
					_dir_path_elem=_dir_path_elem,
				)

	if is_root is True:
		return _path_elems

class PathElem():
	def __init__(
		self,
		elem, 
		path_elem, 
		direpa_root,
		isfile,
		patterns,
		parent=None,
	):
		self._parent=parent
		self.isfile=isfile
		self.elem=elem
		self.path_elem=path_elem
		self.path_text="{}".format(os.path.relpath(path_elem, direpa_root))
		self._level=get_path_level(self.path_text)
		self.is_discarded=False
		if self._parent is not None:
			self.is_discarded=self._parent.is_discarded
		self.is_recursive=self.isfile is False
		self._process_patterns(patterns)

	def _process_patterns(self, patterns):
		for pattern in patterns:
			if pattern.level == -1 or (pattern.level == self._level):
				if not (self.isfile is True and pattern.match_file is False):
					if pattern.is_negate is True:

						if self.is_discarded is True:
							elem=self.path_text
							if pattern.match_reg_elem is True:
								elem=self.elem

							if re.match(pattern.reg_text, elem):
								self.is_discarded=False
								if self.isfile is False:
									self.is_recursive=True
					else:
						elem=self.path_text
						if pattern.match_reg_elem is True:
							elem=self.elem

						if re.match(pattern.reg_text, elem):
							self.is_discarded=True
							if self.isfile is False:
								self.is_recursive=pattern.is_recursive
