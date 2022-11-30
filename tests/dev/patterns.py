#!/usr/bin/env python3
from pprint import pprint
import os
import re
import sys

from .helpers import err

from ..gpkgs import message as msg

def test_patterns(main_pkg):

    for pattern, output in [
        ["", None],
        ["# This is a comment", None],
        ["\# This is not a comment", "# This is not a comment"],
        ["  logs", "logs"],
        ["\  logs", "  logs"],
        ["\!logs", "\!logs"],
        ["!logs", "!logs"],
    ]:
        pattern_text=main_pkg._set_pattern(pattern)
        if pattern_text != output:
            msg.warning("For pattern '{}' at set_attribute expected '{}' obtained '{}'".format(
                pattern, 
                output,
                pattern_text,
            ))
            err()
        msg.success("Passed set_pattern '{}'".format(pattern))

    patterns=[
        dict( pattern=r"/", reg_text="^.*$", is_negate=False, is_recursive=False, level=1, match_file=True, match_reg_elem=False),
        dict( pattern=r"**", reg_text="^.*$", is_negate=False, is_recursive=True, level=-1, match_file=True, match_reg_elem=False),
        dict( pattern=r"**/", reg_text="^.*$", is_negate=False, is_recursive=True, level=-1, match_file=True, match_reg_elem=False),
        dict( pattern=r"/**", reg_text="^.*$", is_negate=False, is_recursive=True, level=-1, match_file=True, match_reg_elem=False),
        dict( pattern=r"/**logs", refinePatternError="pattern '**' must precede a forward slash"),
        dict( pattern=r"**logs/", refinePatternError="pattern '**' must precede a forward slash"),
        dict( pattern=r"**logs", refinePatternError="pattern '**' must precede a forward slash"),
        dict( pattern=r"/logs", reg_text="^logs$", is_negate=False, is_recursive=False, level=1, match_file=True, match_reg_elem=False),
        dict( pattern=r"/logs/debug/", reg_text="^logs/debug$", is_negate=False, is_recursive=False, level=2, match_file=False, match_reg_elem=False),
        dict( pattern=r"\!logs", reg_text="^\!logs$", is_negate=False, is_recursive=False, level=-1, match_file=True, match_reg_elem=True),
        dict( pattern=r"\\!logs", reg_text=r"^\\\!logs$", is_negate=False, is_recursive=False, level=-1, match_file=True, match_reg_elem=True),
        dict( pattern=r"\\\\\\logs", reg_text=r"^\\\\\\logs$", is_negate=False, is_recursive=False, level=-1, match_file=True, match_reg_elem=True),
        dict( pattern=r"\@logs", refinePatternError="escape char is only for symbols"),
        dict( pattern=r"\\\@logs", refinePatternError="escape char is only for symbols"),
        dict( pattern=r"logs\\", reg_text=r"^logs\\$", is_negate=False, is_recursive=False, level=-1, match_file=True, match_reg_elem=True),
        dict( pattern=r"logs/", reg_text=r"^logs$", is_negate=False, is_recursive=False, level=-1, match_file=False, match_reg_elem=True),
        dict( pattern=r"logs/main/debug/", reg_text=r"^logs/main/debug$", is_negate=False, is_recursive=False, level=3, match_file=False, match_reg_elem=False),
        dict( pattern=r"logs//", refinePatternError="not allowed consecutive forward slashes"),
        dict( pattern=r"!logs/", reg_text=r"^logs$", is_negate=True, is_recursive=False, level=-1, match_file=False, match_reg_elem=True),
        dict( pattern=r"\!logs/", reg_text=r"^\!logs$", is_negate=False, is_recursive=False, level=-1, match_file=False, match_reg_elem=True),
        dict( pattern=r"/logs*", reg_text=r"^logs[^/]*$", is_negate=False, is_recursive=False, level=1, match_file=True, match_reg_elem=False),
        dict( pattern=r"/logs**", refinePatternError="pattern '**' must be after a forward slash"),
        dict( pattern=r"/logs/**a/debug", refinePatternError="pattern '**' must precede a forward slash"),
        dict( pattern=r"/logs/**/**", refinePatternError="pattern '**/**' unknown"),
        dict( pattern=r"/l*s", reg_text=r"^l[^/]*s$", is_negate=False, is_recursive=False, level=1, match_file=True, match_reg_elem=False),
        dict( pattern=r"/lo**/debug", refinePatternError="pattern '**' must be after a forward slash"),
        dict( pattern=r"/logs/***", refinePatternError="pattern '***' unknown"),
        dict( pattern=r"/logs/**/**/debug", refinePatternError="pattern '**/**' unknown"),
        dict( pattern=r"/**/**/debug", refinePatternError="pattern '**/**' unknown"),
        dict( pattern=r"/logs/**", reg_text=r"^logs/.*$", is_negate=False, is_recursive=True, level=-1, match_file=True, match_reg_elem=False),
        dict( pattern=r"/logs/**/debug", reg_text=r"^logs/(.*/)?debug$", is_negate=False, is_recursive=True, level=-1, match_file=True, match_reg_elem=False),
        dict( pattern=r"**/logs/**/debug", reg_text=r"^(.*/)?logs/(.*/)?debug$", is_negate=False, is_recursive=True, level=-1, match_file=True, match_reg_elem=False),
        dict( pattern=r"**/logs/**debug", refinePatternError="'**' must precede a forward slash"),
        dict( pattern=r"**/logs/*debug", reg_text=r"^(.*/)?logs/[^/]*debug$", is_negate=False, is_recursive=True, level=-1, match_file=True, match_reg_elem=False),
        dict( pattern=r"d??u?/", reg_text=r"^d[^/]{1}[^/]{1}u[^/]{1}$", is_negate=False, is_recursive=False, level=-1, match_file=False, match_reg_elem=True),
        dict( pattern=r"[a-z", refinePatternError="uncomplete range pattern"),
        dict( pattern=r"[]", refinePatternError="error empty range pattern"),
        dict( pattern=r"[a-zA-Z0-9-]", reg_text=r"^[a-zA-Z0-9-]$", is_negate=False, is_recursive=False, level=-1, match_file=True, match_reg_elem=True),
        dict( pattern=r"[a-z@]", refinePatternError="unknown char"),
        dict( pattern=r"{debug}/", reg_text=r"^\{debug\}$", is_negate=False, is_recursive=False, level=-1, match_file=False, match_reg_elem=True),
        dict( pattern=r'"debug"', reg_text=r"^\"debug\"$", is_negate=False, is_recursive=False, level=-1, match_file=True, match_reg_elem=True),
        dict( pattern=r"'debug'", reg_text=r"^\'debug\'$", is_negate=False, is_recursive=False, level=-1, match_file=True, match_reg_elem=True),
        dict( pattern=r"build/debug", reg_text=r"^build/debug$", is_negate=False, is_recursive=False, level=2, match_file=True, match_reg_elem=False),
        dict( pattern=r"**/logs", reg_text=r"^(.*/)?logs$", is_negate=False, is_recursive=True, level=-1, match_file=True, match_reg_elem=False),
        dict( pattern=r"**/logs/debug.log", reg_text=r"^(.*/)?logs/debug\.log$", is_negate=False, is_recursive=True, level=-1, match_file=True, match_reg_elem=False),
        dict( pattern=r"*.log", reg_text=r"^[^/]*\.log$", is_negate=False, is_recursive=False, level=-1, match_file=True, match_reg_elem=True),
        dict( pattern=r"/debug.log", reg_text=r"^debug\.log$", is_negate=False, is_recursive=False, level=1, match_file=True, match_reg_elem=False),
        dict( pattern=r"debug.log", reg_text=r"^debug\.log$", is_negate=False, is_recursive=False, level=-1, match_file=True, match_reg_elem=True),
        dict( pattern=r"debug?.log", reg_text=r"^debug[^/]{1}\.log$", is_negate=False, is_recursive=False, level=-1, match_file=True, match_reg_elem=True),
        dict( pattern=r"debug[0-9].log", reg_text=r"^debug[0-9]\.log$", is_negate=False, is_recursive=False, level=-1, match_file=True, match_reg_elem=True),
        dict( pattern=r"debug[01].log", reg_text=r"^debug[01]\.log$", is_negate=False, is_recursive=False, level=-1, match_file=True, match_reg_elem=True),
        dict( pattern=r"debug[!01].log", reg_text=r"^debug[^01]\.log$", is_negate=False, is_recursive=False, level=-1, match_file=True, match_reg_elem=True),
        dict( pattern=r"debug[a-z].log", reg_text=r"^debug[a-z]\.log$", is_negate=False, is_recursive=False, level=-1, match_file=True, match_reg_elem=True),
        dict( pattern=r"logs", reg_text=r"^logs$", is_negate=False, is_recursive=False, level=-1, match_file=True, match_reg_elem=True),
        dict( pattern=r"logs/", reg_text=r"^logs$", is_negate=False, is_recursive=False, level=-1, match_file=False, match_reg_elem=True),
        dict( pattern=r"logs/**/debug.log", reg_text=r"^logs/(.*/)?debug\.log$", is_negate=False, is_recursive=True, level=-1, match_file=True, match_reg_elem=False),
        dict( pattern=r"logs/*day/debug.log", reg_text=r"^logs/[^/]*day/debug\.log$", is_negate=False, is_recursive=False, level=3, match_file=True, match_reg_elem=False),
        dict( pattern=r"logs/debug.log", reg_text=r"^logs/debug\.log$", is_negate=False, is_recursive=False, level=2, match_file=True, match_reg_elem=False),
        dict( pattern=r"!/logs", reg_text=r"^logs$", is_negate=True, is_recursive=False, level=1, match_file=True, match_reg_elem=False),
    ]

    for dy_pattern in patterns:
        try:
            pattern_text=main_pkg._set_pattern(dy_pattern["pattern"])
            if pattern_text is not None:
                pattern=main_pkg._Pattern(pattern_text)
                for attr in [
                    "is_negate",
                    "is_recursive",
                    "level",
                    "match_file",
                    "match_reg_elem",
                    "reg_text",
                ]:
                    try:
                        if getattr(pattern, attr) != dy_pattern[attr]:
                            msg.warning("For pattern '{}' at attribute '{}' expected '{}' obtained '{}'".format(
                                dy_pattern["pattern"], 
                                attr, 
                                dy_pattern[attr],
                                getattr(pattern, attr),
                            ))
                            err()
                    except KeyError:
                        print()
                        print("pattern:")
                        pprint(dy_pattern)
                        print()
                        print("object:")
                        pprint(dict(
                            is_negate=pattern.is_negate,
                            level=pattern.level,
                            match_file=pattern.match_file,
                            reg_text=pattern.reg_text,
                        ))
                        print()
                        raise

                msg.success("Passed Pattern '{}'".format(dy_pattern["pattern"]))
        except main_pkg.RefinePatternError as e:
            if "refinePatternError" in dy_pattern:
                if dy_pattern["refinePatternError"] in str(e):
                    msg.success("Passed Pattern '{}'".format(dy_pattern["pattern"]))
                else:
                    msg.error("For pattern '{}' excepted message '{}'.".format(dy_pattern["pattern"], dy_pattern["refinePatternError"]))
                    raise
            else:
                msg.error("For pattern '{}' unmanaged error.".format(dy_pattern["pattern"]))
                raise
   