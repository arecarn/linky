import pytest
import util

import sys
import os
sys.path.insert(0, os.path.abspath('..'))
import dploy


@pytest.fixture(scope='module')
def source_a(request):
    tree = [
        {
            'source_a' : [
                {
                    'aaa': [
                        'aaa',
                        'bbb',
                        {
                            'ccc': [
                                'aaa',
                                'bbb',
                            ],
                        },
                    ],
                },
            ],
        },
    ]
    util.create_tree(tree)

    def source_a_teardown():
        util.remove_tree('source_a')
    request.addfinalizer(source_a_teardown)


@pytest.fixture(scope='module')
def source_b(request):
    tree = [
        {
            'source_b' : [
                {
                    'aaa': [
                        'ddd',
                        'eee',
                        {
                            'fff': [
                                'aaa',
                                'bbb',
                            ],
                        },
                    ],
                },
            ],
        },
    ]
    util.create_tree(tree)

    def source_b_teardown():
        util.remove_tree('source_b')
    request.addfinalizer(source_b_teardown)


@pytest.fixture(scope='module')
def dest(request):
    util.create_directory('dest')

    def dest_teardown():
        util.remove_tree('dest')
    request.addfinalizer(dest_teardown)


def test_test(source_a, dest):
    dploy.dploy('source_a', 'dest')
    assert os.path.islink('dest/aaa')


def test_dploy_twice(source_a, dest):
    dploy.dploy('source_a', 'dest')
    dploy.dploy('source_a', 'dest')
    assert os.path.islink('dest/aaa')
    dploy.dploy('source_a', 'dest')
    assert os.path.islink('dest/aaa')

    assert os.path.isfile('dest/aaa/aaa')
    assert os.path.isfile('dest/aaa/bbb')
    assert os.path.isdir('dest/aaa/ccc')

    dploy.dploy('source_b', 'dest')
    assert os.path.isdir('dest/aaa')

    assert os.path.islink('dest/aaa/aaa')
    assert os.path.islink('dest/aaa/bbb')
    assert os.path.islink('dest/aaa/ccc')

    assert os.path.islink('dest/aaa/ddd')
    assert os.path.islink('dest/aaa/eee')
    assert os.path.islink('dest/aaa/fff')