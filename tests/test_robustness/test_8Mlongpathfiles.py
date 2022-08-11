#!/usr/bin/env python3
# encoding: utf-8
import errno
import sys
from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest
from nose import with_setup
from tests.utils import *

NUMPAIRS = 1024+1

def branch_tree(current_path, remaining_depth):
    if (remaining_depth > 0):
        for i in range(2):
            next_path = current_path + "long" * 4 + str(i) + "/"
            create_dirs (next_path)
            branch_tree (next_path, remaining_depth - 1)
    else:
        for i in range(NUMPAIRS):
            create_file(str(i).zfill(1 + i), current_path + 'a' + str(i).zfill(7))
            create_file(str(i).zfill(1 + i), current_path + 'b' + str(i).zfill(7))
            create_link(current_path + 'a' + str(i).zfill(7), current_path + 'c' + str(i).zfill(7))
            create_link(current_path + 'a' + str(i).zfill(7), current_path + 'd' + str(i).zfill(7))
            create_link(current_path + 'a' + str(i).zfill(7), current_path + 'e' + str(i).zfill(7))
            create_link(current_path + 'a' + str(i).zfill(7), current_path + 'f' + str(i).zfill(7))
            create_link(current_path + 'b' + str(i).zfill(7), current_path + 'g' + str(i).zfill(7))
            create_link(current_path + 'b' + str(i).zfill(7), current_path + 'h' + str(i).zfill(7))


@attr('slow')
@with_setup(usual_setup_func, usual_teardown_func)
def test_manylongpathfiles():
    max_depth = 10 # will give 8M files total if NUMPAIRS = 1024+1
    try:
        branch_tree ("", max_depth)
    except OSError as e:
        if e.errno == errno.ENOSPC:
            raise SkipTest('not enough space in testdir')
        raise

    head, *data, footer = run_rmlint('-c json:no_body')
    assert footer['duplicates'] + footer['duplicate_sets'] == NUMPAIRS * 2 ** max_depth * 8
