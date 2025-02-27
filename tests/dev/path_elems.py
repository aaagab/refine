#!/usr/bin/env python3
from pprint import pprint
import os
import sys
import tempfile

from .helpers import err

from ...dev.refine import PathElem
from ...dev.patterns import Pattern, set_pattern

from ...gpkgs import message as msg
from ...gpkgs import shell_helpers as shell

def test_path_elems():
    direpa_tmp=os.path.join(
        tempfile.gettempdir(),
        "refine",
    )

    if os.path.exists(direpa_tmp):
        shell.rmtree(direpa_tmp)
    os.makedirs(direpa_tmp, exist_ok=True)

    _paths=[
        ".log",
        "build/",
        "build/logs/",
        "build/logs/debug.log",
        "build/logs/foo.bar",
        "build/logs/latest/",
        "build/logs/latest/debug.log",
        "debug.log",
        "debug0.log",
        "debug01.log",
        "debug1.log",
        "debug10.log",
        "debug2.log",
        "debuga.log",
        "debugb.log",
        "debugg.log",
        "foo.log",
        "important/",
        "important/debug.log",
        "important/trace.log",
        "important.log",
        "logs/",
        "logs/build/",
        "logs/build/debug.log",
        "logs/build/logs/",
        "logs/build/logs/debug.log",
        "logs/debug.log",
        "logs/important.log",
        "logs/latest/",
        "logs/latest/debug.log",
        "logs/latest/foo.bar",
        "logs/monday/",
        "logs/monday/debug.log",
        "logs/monday/foo.bar",
        "logs/monday/pm/",
        "logs/monday/pm/debug.log",
        "logs/tuesday/",
        "logs/tuesday/debug.log",
        "trace.log",
    ]

    for _path in _paths:
        _path_elem=os.path.join(direpa_tmp, _path)
        if _path[-1] == "/":
            os.makedirs(_path_elem, exist_ok=True)
        else:
            open(_path_elem, "w").close()

    path_elems=[
        dict(path_elem="logs/debug.log", patterns=["**/logs"], elem="logs", is_discarded=True, isfile=None, is_recursive=True, parent=None),
        dict(path_elem="logs/monday/foo.bar", patterns=["**/logs"], elem="logs", is_discarded=True, isfile=None, is_recursive=True, parent=None),
        dict(path_elem="build/logs/debug.log", patterns=["**/logs"], elem="build/logs", is_discarded=True, isfile=None, is_recursive=True, parent=None),
        dict(path_elem="logs/debug.log", patterns=["**/logs/debug.log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="build/logs/debug.log", patterns=["**/logs/debug.log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="logs/build/debug.log", patterns=["**/logs/debug.log"], elem=None, is_discarded=False, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="logs/build", patterns=["**/logs"], elem=None, is_discarded=False, isfile=False, is_recursive=True, parent=None),
        dict(path_elem="debug.log", patterns=["*.log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="foo.log", patterns=["*.log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem=".log", patterns=["*.log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="logs/debug.log", patterns=["*.log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="debug.log", patterns=["/debug.log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="logs/debug.log", patterns=["/debug.log"], elem=None, is_discarded=False, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="debug.log", patterns=["debug.log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="logs/debug.log", patterns=["debug.log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="debug0.log", patterns=["debug?.log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="debugg.log", patterns=["debug?.log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="debug10.log", patterns=["debug?.log"], elem=None, is_discarded=False, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="debug0.log", patterns=["debug[0-9].log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="debug1.log", patterns=["debug[0-9].log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="debug10.log", patterns=["debug[0-9].log"], elem=None, is_discarded=False, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="debug0.log", patterns=["debug[01].log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="debug1.log", patterns=["debug[01].log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="debug2.log", patterns=["debug[01].log"], elem=None, is_discarded=False, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="debug01.log", patterns=["debug[01].log"], elem=None, is_discarded=False, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="debug2.log", patterns=["debug[!01].log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="debug0.log", patterns=["debug[!01].log"], elem=None, is_discarded=False, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="debug1.log", patterns=["debug[!01].log"], elem=None, is_discarded=False, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="debug01.log", patterns=["debug[!01].log"], elem=None, is_discarded=False, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="debuga.log", patterns=["debug[a-z].log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="debugb.log", patterns=["debug[a-z].log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="debug1.log", patterns=["debug[a-z].log"], elem=None, is_discarded=False, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="logs", patterns=["logs"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="logs/debug.log", patterns=["logs"], elem="logs", is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="logs/latest/foo.bar", patterns=["logs"], elem="logs", is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="build/logs", patterns=["logs"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="build/logs/debug.log", patterns=["logs"], elem="build/logs", is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="logs/debug.log", patterns=["logs/"], elem="logs", is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="logs/latest/foo.bar", patterns=["logs/"], elem="logs", is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="build/logs/foo.bar", patterns=["logs/"], elem="build/logs", is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="build/logs/latest/debug.log", patterns=["logs/"], elem="build/logs", is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="logs/debug.log", patterns=["logs/**/debug.log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="logs/monday/debug.log", patterns=["logs/**/debug.log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="logs/monday/pm/debug.log", patterns=["logs/**/debug.log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="logs/monday/debug.log", patterns=["logs/*day/debug.log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="logs/tuesday/debug.log", patterns=["logs/*day/debug.log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="logs/latest/debug.log", patterns=["logs/*day/debug.log"], elem=None, is_discarded=False, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="logs/debug.log", patterns=["logs/debug.log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="debug.log", patterns=["logs/debug.log"], elem=None, is_discarded=False, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="build/logs/debug.log", patterns=["logs/debug.log"], elem=None, is_discarded=False, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="debug.log", patterns=["*.log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="trace.log", patterns=["*.log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="important.log", patterns=["*.log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="logs/important.log", patterns=["*.log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="debug.log", patterns=["*.log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="important/trace.log", patterns=["*.log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="important/debug.log", patterns=["*.log"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="debug.log", patterns=["trace.*"], elem=None, is_discarded=False, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="important/trace.log", patterns=["trace.*"], elem=None, is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="important/debug.log", patterns=["trace.*"], elem=None, is_discarded=False, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="logs/debug.log", patterns=["logs/"], elem="logs", is_discarded=True, isfile=None, is_recursive=False, parent=None),
        dict(path_elem="logs/important.log", patterns=["logs/"], elem="logs", is_discarded=True, isfile=None, is_recursive=False, parent=None),
    ]

    for dy_elem in path_elems:
        direpa_root=direpa_tmp

        tmp_path_elem:str
        assert isinstance(dy_elem["path_elem"], str)
        assert isinstance(dy_elem["elem"], str) or dy_elem["elem"] is None
        if dy_elem["elem"] is None:
            tmp_path_elem=os.path.join(direpa_root, dy_elem["path_elem"])
        else:
            tmp_path_elem=os.path.join(direpa_root, dy_elem["elem"])

        if os.path.exists(tmp_path_elem) is False:
            msg.error("Path not found '{}'".format(tmp_path_elem), exit=1)
        dy_elem["isfile"]=os.path.isfile(tmp_path_elem)

        tmp_patterns=[]
        assert isinstance(dy_elem["patterns"], list)
        for pattern in dy_elem["patterns"]:
            pattern_text=set_pattern(pattern)
            if pattern_text is not None:
                tmp_patterns.append(Pattern(pattern_text))

        assert isinstance(dy_elem["parent"], PathElem) or dy_elem["parent"] is None
        path_elem=PathElem(
            direpa_root=direpa_root,
            elem=tmp_path_elem.split(os.sep)[-1],
            isfile=dy_elem["isfile"],
            patterns=tmp_patterns,
            path_elem=tmp_path_elem,
            parent=dy_elem["parent"],
        )

        for attr in [
            "is_discarded",
            "is_recursive",
        ]:
            if getattr(path_elem, attr) != dy_elem[attr]:
                print()
                print("  path_elem: {}".format(
                    dy_elem["path_elem"],
                ))

                print()
                print("  patterns:")
                for pattern in tmp_patterns:
                    print("    {}    {}".format(pattern.pattern, pattern.reg_text))

                print()
                print("  tested: {}  isfile: {}".format(
                    tmp_path_elem[len(direpa_root)+1:],
                    os.path.isfile(tmp_path_elem),
                ))

                print()
                msg.warning("For attribute '{}' expected '{}' obtained '{}'".format(
                    attr, 
                    dy_elem[attr],
                    getattr(path_elem, attr), 
                ))
                print()
                err()

        msg.success("Passed PathElem '{}'".format(dy_elem["path_elem"]))
        