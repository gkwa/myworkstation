import pytest

import packages


@pytest.fixture(scope='module')
def package_store():
    return packages.PackageStore()


def test_write_file(package_store):
    package_store.write_single_file(packages.ansible)
    assert packages.ansible.basename == 'playbook{}.yml'


def test_write_files(package_store):
    package_store.write_split_files(packages.ansible)
