#!/usr/bin/env python3
import os
from pprint import pprint
import re
import sys

from .exceptions import RefinePatternError

def set_pattern(line):
	sline=line.strip()
	if sline != "":
		if sline[0] != "#":
			if sline[:2] == "\\#":
				sline=sline[1:]
			elif sline[:2] == "\\ ":
				sline=sline[1:]
			return sline
	return None	

class Pattern():
	def __init__(self, pattern):
		self.is_negate=False
		self.is_recursive=False
		self.level=-1
		self.match_file=False
		self.match_reg_elem=False
		self.reg_text=""
		self.pattern=pattern

		self._after_slash=False
		self._after_stars=False
		self._escaped=False
		self._escaped_chars=[
			"!",
			"*",
			"?",
			"\\",
			"[",
			"]",
		]
		self._index=0
		self._is_absolute=False
		self._is_stars=False
		self._reg_range=r"[a-zA-Z0-9-]"

		self._parse_pattern()

	def _get_len_remain(self):
		return len(self.pattern) - 1 - self._index

	def _is_first_ch(self):
		return self._index == 0

	def _is_last_ch(self, _index=None):
		if _index is None:
			_index=self._index
		return _index == len(self.pattern) -1

	def _peek(self, num=1):
		return self.pattern[self._index+num]

	def _parse_pattern(self):
		ch=self.pattern[self._index]

		if self._escaped is True:
			self._escaped=False
			if ch in self._escaped_chars:
				self.reg_text+="\{}".format(ch)
				if ch == "/":
					self._after_slash=True
			else:
				raise RefinePatternError("In pattern '{}' escape char is only for symbols {} not for {}.".format(
					self.pattern,
					self._escaped_chars,
					repr(ch),
				))
		else:
			if ch != "*":
				self._after_stars=False
				self._after_slash=False

			if ch == "\\":
				self._escaped=True
			elif ch == "/":
				self._after_slash=True
				if self._is_last_ch() is True:
					if self._is_first_ch() is True:
						self._is_absolute=True
						self.reg_text+=".*"
						self.match_file=True
				else:
					self._is_absolute=True
					if self._peek() == "/":
						raise RefinePatternError("In pattern '{}' not allowed consecutive forward slashes.".format(self.pattern))
					if self._is_first_ch() is True:
						pass
					elif self._index == 1 and self.is_negate is True:
						pass
					else:
						self.reg_text+=ch
			elif ch == "!":
				if self._index == 0:
					self.is_negate=True
				else:
					self.reg_text+="\{}".format(ch)
			elif ch == "*":
				len_remain=self._get_len_remain()
				if len_remain == 0:
					self.reg_text+="[^/]*"
					self._after_stars=False
				elif len_remain == 1:
					if self._peek() == "*":
						if self._after_slash is False and self._is_first_ch() is False:
							raise RefinePatternError("In pattern '{}' pattern '**' must be after a forward slash.".format(self.pattern))
						if self._after_stars is True:
							raise RefinePatternError("In pattern '{}' pattern '**/**' unknown.".format(self.pattern))
						else:
							self._is_absolute=True
							self._is_stars=True
							self.reg_text+=".*"
							self._index+=1
					else:
						self.reg_text+="[^/]*"
						self._after_stars=False
				elif len_remain >= 2:
					if self._peek() == "*":
						if self._after_slash is False and self._is_first_ch() is False:
							raise RefinePatternError("In pattern '{}' pattern '**' must be after a forward slash.".format(self.pattern))
						if self._peek(2) == "*":
							raise RefinePatternError("In pattern '{}' pattern '***' unknown.".format(self.pattern))
						elif self._peek(2) == "/":
							if self._after_stars is True:
								raise RefinePatternError("In pattern '{}' pattern '**/**' unknown.".format(self.pattern))

							self._is_absolute=True
							self._is_stars=True
							if len_remain == 2:
								self.reg_text+=".*"
							else:
								self.reg_text+="(.*/)?"
							self._index+=2
							self._after_stars=True
						else:
							raise RefinePatternError("In pattern '{}' pattern '**' must precede a forward slash.".format(self.pattern))
					else:
						self.reg_text+="[^/]*"
						self._after_stars=False
			elif ch == "?":
				self.reg_text+="[^/]{1}"
			elif ch in ["["]:
				_pattern=ch
				for i in range(1, self._get_len_remain()+1):
					tmp_ch=self._peek(i)
					_pattern+=tmp_ch
					if self._is_last_ch(self._index+i) is True and tmp_ch != "]":
						raise RefinePatternError("In pattern '{}' uncomplete range pattern '{}' .".format(self.pattern, _pattern))
					elif tmp_ch == "]":
						if _pattern == "[]":
							raise RefinePatternError("In pattern '{}' error empty range pattern '{}'.".format(self.pattern, _pattern))
						else:
							self.reg_text+=_pattern
							self._index+=i
							break
					elif re.match(self._reg_range, tmp_ch):
						pass
					else:
						if tmp_ch == "!" and i == 1:
							_pattern=_pattern[:-1]+"^"
						else:
							raise RefinePatternError("In pattern '{}' at range pattern '{}' unknown char '{}'.".format(self.pattern, _pattern, tmp_ch))
			elif ch == "'":
				self.reg_text+="\\{}".format(ch)
			elif ch in [
				".",
				"+",
				"|",
				"{",
				"}",
				"(",
				")",
				"^",
				"$",
				"]",
				"\"",
				"=",
			]:
				self.reg_text+="\{}".format(ch)
			else:
				self.reg_text+=ch

		if self._is_last_ch() is True:
			self.reg_text="^{}$".format(self.reg_text)
			if self._is_stars is True:
				self.match_file=True
				self.is_recursive=True	
			else:
				self.is_recursive=False
				if ch != "/":
					self.match_file=True
				if self._is_absolute is True:
					if self.is_negate is True:
						self.level=get_path_level(self.pattern[1:])
					else:
						self.level=get_path_level(self.pattern)
				else:
					self.match_reg_elem=True
		else:
			self._index+=1
			return self._parse_pattern()

def get_path_level(path_elem):
	level=0
	for elem in path_elem.split("/"):
		if elem != "":
			level+=1
	if level == 0:
		level=1
	return level
