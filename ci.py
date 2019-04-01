#!/usr/bin/env python

from jinja2 import Template

import ansible
import bundle
from packages import PackageStore

AZURE_FILENAME = 'azure-pipelines.yml'
TRAVIS_FILENAME = '.travis.yml'

STR_BREW_BUNDLE_TRAVIS = """{#- jinja2 -#}
# Don't edit, this.  Edit list.yml and run ./main.py to generate this.

language: ruby
cache: bundler
sudo: required
dist: trusty
group: edge
os: osx
osx_image: xcode10.2
env:
{%- for filename in splits %}
- BREWFILE={{ filename }}
{%- endfor %}
script:
- travis_retry brew bundle --verbose --file=$BREWFILE
"""

STR_ANSIBLE_TRAVIS = """{#- jinja2 -#}
# Don't edit, this.  Edit list.yml and run ./main.py to generate this.

language: ruby
cache: bundler
sudo: required
dist: trusty
group: edge
os: osx
osx_image: xcode10.2
env:
{%- for filename in splits %}
- PLAYBOOK={{ filename }}
{%- endfor %}
script:
- travis_retry ansible-playbook --verbose --verbose $PLAYBOOK
"""

STR_BREW_BUNDLE_AZURE = """{#- jinja2 -#}
trigger:
- master
pool:
  vmImage: macOS-10.14
strategy:
  matrix:
{%- for filename in splits %}
    set_env_to_{{ filename }}:
      BREWFILE: {{ filename }}
{%- endfor %}
steps:
- script: brew bundle --verbose --file=$BREWFILE
"""

STR_BREW_ANSIBLE_AZURE = """{#- jinja2 -#}
trigger:
- master
pool:
  vmImage: macOS-10.14
strategy:
  matrix:
{%- for filename in splits %}
    set_env_to_{{ filename }}:
      PLAYBOOK: '{{ filename }}'
{%- endfor %}
steps:
- script: ansible-playbook --verbose --verbose $PLAYBOOK
"""


def write_azure_bundle(store, bundle):
    flist = store.split_targets(bundle.config_basename)
    out = Template(STR_BREW_BUNDLE_AZURE).render({'splits': flist})
    with open(AZURE_FILENAME, 'w') as fh:
        fh.write(out)


def write_azure_ansible(store, ansible):
    flist = store.split_targets(ansible.config_basename)
    out = Template(STR_BREW_ANSIBLE_AZURE).render({'splits': flist})
    with open(AZURE_FILENAME, 'w') as fh:
        fh.write(out)


def write_travis_bundle(store, bundle):
    flist = store.split_targets(bundle.config_basename)
    out = Template(STR_BREW_BUNDLE_TRAVIS).render({'splits': flist})
    with open(TRAVIS_FILENAME, 'w') as fh:
        fh.write(out)


def write_travis_ansible(store, ansible):
    flist = store.split_targets(ansible.config_basename)
    out = Template(STR_ANSIBLE_TRAVIS).render({'splits': flist})
    with open(TRAVIS_FILENAME, 'w') as fh:
        fh.write(out)


def write_all_files(store, bdl, ans):
    write_travis_bundle(store, bdl)
    write_travis_ansible(store, ans)
    write_azure_ansible(store, ans)
    write_azure_bundle(store, bdl)


def main():
    store = PackageStore()
    ans = ansible.Ansible(store)
    bdl = bundle.Bundle(store)
    write_all_files(store, bdl, ans)


if __name__ == "__main__":
    main()
