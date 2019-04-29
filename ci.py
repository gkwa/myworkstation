from jinja2 import Template


class MyBase(object):
    def __init__(self, preamble, *args, **kwargs):
        self.preamble = preamble
        self.filename = kwargs['filename']
        self.template = Template(kwargs['tpl_splits_str'])

    def write_config(self, splits):
        rendered = self.template.render({
            'preamble': Template(self.preamble).render(),
            'splits': splits,
        })
        with open(self.filename, 'w') as config:
            config.write(rendered)


class Azure(MyBase):
    def __init__(self, tpl_str="""{#- jinja2 -#}
# Don't edit, this.  Edit list.yml and run ./main.py to generate this.

trigger:
- master
pool:
  vmImage: macOS-10.14
strategy:
  matrix:
""", filename='azure-pipelines.yml'):
        self.filename = filename
        self.tpl_splits_str = tpl_str
        self.tpl_preamble_str = """{#- jinja2 -#}
# Don't edit, this.  Edit list.yml and run ./main.py to generate this.

trigger:
- master
pool:
  vmImage: macOS-10.14
strategy:
  matrix:
"""
        MyBase.__init__(self, self.tpl_preamble_str,
                        tpl_splits_str=self.tpl_splits_str,
                        filename=self.filename)


class Travis(MyBase):
    def __init__(self, tpl_str="""{#- jinja2 -#}
# Don't edit, this.  Edit list.yml and run ./main.py to generate this.

trigger:
- master
pool:
  vmImage: macOS-10.14
strategy:
  matrix:
""", filename='.travis.yml'):
        self.filename = filename
        self.tpl_splits_str = tpl_str
        self.tpl_preamble_str = """{#- jinja2 -#}
# Don't edit, this.  Edit list.yml and run ./main.py to generate this.

language: ruby
cache: bundler
sudo: required
dist: trusty
group: edge
os: osx
osx_image: xcode10.2
env:
"""
        MyBase.__init__(self, self.tpl_preamble_str,
                        tpl_splits_str=self.tpl_splits_str,
                        filename=self.filename)


class TravisAnsible(Travis):
    def __init__(self):
        Travis.__init__(self, """{#- jinja2 -#}
{{preamble}}
{%- for filename in splits %}
- PLAYBOOK={{ filename }}
{%- endfor %}
script:
- travis_retry ansible-playbook --verbose --verbose $PLAYBOOK""")


class TravisBundle(Travis):
    def __init__(self):
        Travis.__init__(self, """{#- jinja2 -#}
{{preamble}}
{%- for filename in splits %}
- BREWFILE={{ filename }}
{%- endfor %}
script:
- travis_retry brew bundle --verbose --file=$BREWFILE
""")


class AzureAnsible(Azure):
    def __init__(self):
        Azure.__init__(self, """{#- jinja2 -#}
{{preamble}}
{%- for filename in splits %}
    set_env_to_{{ filename }}:
      PLAYBOOK: '{{ filename }}'
{%- endfor %}
steps:
- script: ansible-playbook --verbose --verbose $PLAYBOOK
""")


class AzureBundle(Azure):
    def __init__(self):
        Azure.__init__(self, """{#- jinja2 -#}
{{preamble}}
{%- for filename in splits %}
    set_env_to_{{ filename }}:
      BREWFILE: {{ filename }}
{%- endfor %}
steps:
- script: brew bundle --verbose --file=$BREWFILE
""")
