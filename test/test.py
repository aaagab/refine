#!/usr/bin/env python3
# author: Gabriel Auger
# version: 3.3.0
# name: refine
# license: MIT

import os
from pprint import pprint
import glob
import re
# from modules.refine import copy_to_destination, get_paths_to_copy

if __name__ == "__main__":
    import sys, os
    import importlib
    direpa_script_parent=os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    module_name=os.path.basename(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    sys.path.insert(0, direpa_script_parent)
    pkg = importlib.import_module(module_name)
    del sys.path[0]

    direpa_script=os.path.dirname(os.path.realpath(__file__))
    direpa_copy=os.path.dirname(direpa_script)
    print(direpa_copy)
    # pprint(pkg.get_paths_to_copy(direpa_copy, use_files=False))
    pprint(
    pkg.get_paths_to_copy(direpa_copy)
        )

    # direpa_src=r"C:\Users\user\Desktop\data\apps\r\refine\src"
    # rule="**\.env"

        # 'C:\\Users\\user\\Desktop\\data\\apps\\r\\refine\\src\\dev\\__pycache__',

    # excluded_dirs={
    #     # r'C:\Users\user\Desktop\data\apps\r\refine\src\__pycache__',
    #     'C:\\Users\\user\\Desktop\\data\\apps\\r\\refine\\src\\gpkgs\\message\\__pycache__',
    #     # 'C:\\Users\\user\\Desktop\\data\\apps\\r\\refine\\src\\gpkgs\\message\\dev\\__pycache__',
    #     # 'C:\\Users\\user\\Desktop\\data\\apps\\r\\refine\\src\\gpkgs\\message\\gpkgs\\format_text\\__pycache__',
    #     # 'C:\\Users\\user\\Desktop\\data\\apps\\r\\refine\\src\\gpkgs\\message\\gpkgs\\format_text\\dev\\__pycache__',
    #     # 'C:\\Users\\user\\Desktop\\data\\apps\\r\\refine\\src\\gpkgs\\shell_helpers\\__pycache__',
    #     # 'C:\\Users\\user\\Desktop\\data\\apps\\r\\refine\\src\\gpkgs\\shell_helpers\\dev\\__pycache__',
    #     # 'C:\\Users\\user\\Desktop\\data\\apps\\r\\refine\\src\\gpkgs\\shell_helpers\\gpkgs\\message\\__pycache__',
    #     # 'C:\\Users\\user\\Desktop\\data\\apps\\r\\refine\\src\\gpkgs\\shell_helpers\\gpkgs\\message\\dev\\__pycache__',
    #     # 'C:\\Users\\user\\Desktop\\data\\apps\\r\\refine\\src\\gpkgs\\shell_helpers\\gpkgs\\message\\gpkgs\\format_text\\__pycache__',
    #     # 'C:\\Users\\user\\Desktop\\data\\apps\\r\\refine\\src\\gpkgs\\shell_helpers\\gpkgs\\message\\gpkgs\\format_text\\dev\\__pycache__'
    # }
    # pkg.my_glob.glob(excluded_dirs, "{}/{}".format(direpa_src, rule), recursive=True)
    # path_name="{}/{}".format(direpa_src, rule)
    # path_name="C:/Users/user/Desktop/data/apps/r/refine/src/**/.env"
    # path_name="**/.env"
    # print(path_name)
    # pkg.my_glob.glob(excluded_dirs, path_name , recursive=True)
    # re.match("C\:\Users\user\Desktop\data\apps\r\refine\src\__pycache__*", ".")
    # re.match("C:/Users/user/Desktop/data/apps/r/refine/src/__pycache__*", ".")
    # re.compile(path_name)
    # print(glob.glob("{}/{}".format(direpa_src, rule), recursive=True))