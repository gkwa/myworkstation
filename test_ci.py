import pytest
import packages
import ci


@pytest.fixture(scope='module')
def azure_ansible():
    return ci.AzureAnsible()


@pytest.fixture(scope='module')
def azure_bundle():
    return ci.AzureBundle()


@pytest.fixture(scope='module')
def travis_ansible():
    return ci.TravisAnsible()


@pytest.fixture(scope='module')
def travis_bundle():
    return ci.TravisBundle()


def test_TravisAnsible(travis_ansible):
    assert travis_ansible.filename == '.travis.yml'
    ps = packages.PackageStore()
    basename = packages.ansible[0]
    splits = ps.split_targets(basename)
    travis_ansible.write_config(splits=splits)


def test_TravisBundle(travis_bundle):
    assert travis_bundle.filename == '.travis.yml'
    ps = packages.PackageStore()
    basename = packages.bundle[0]
    splits = ps.split_targets(basename)
    travis_bundle.write_config(splits=splits)


def test_AzureAnsible(azure_ansible):
    assert azure_ansible.filename == 'azure-pipelines.yml'
    ps = packages.PackageStore()
    basename = packages.ansible[0]
    splits = ps.split_targets(basename)
    azure_ansible.write_config(splits=splits)


def test_AzureBundle(azure_bundle):
    assert azure_bundle.filename == 'azure-pipelines.yml'
    ps = packages.PackageStore()
    basename = packages.bundle[0]
    splits = ps.split_targets(basename)
    azure_bundle.write_config(splits=splits)
