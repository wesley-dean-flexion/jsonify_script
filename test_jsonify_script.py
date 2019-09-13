#!/usr/bin/env python

## @file test_jsonify_script.py
#  @author Wes Dean <wdean@flexion.us>
#  @brief perform unit tests on jsonify_script.py

import pytest
from jsonify_script import *

def test_script_name1():
    assert script_name(
        '/path/to/script/awesome_script.groovy') == 'awesome_script'

def test_script_name2():
    assert script_name(
        '/path/to/script/awesome.script.groovy') == 'awesome.script'

def test_script_name3():
    assert script_name('/path/script/.bashrc') == '.bashrc'

def test_script_type1():
    assert script_type('/path/script/awesome_script.groovy') == 'groovy'

def test_script_type2():
    assert script_type('/path/script/awesome.script.groovy') == 'groovy'

def test_script_type3():
    assert script_type('/path/script/.bashrc') == ''


if __name__ == '__main__':
    pytest.main()
