from itertools import zip_longest

import jinja2

import common

MAX_PACKAGES_PER_GROUP = 60

TPL_STR1 = '''{#- jinja2 -#}
{%- set NEWLINE='\n' -%}
# Don't edit, this.  Edit list.yml and run ./main.py to generate this.
---

{% if tap -%}
- homebrew_tap:
  name: {% for t in tap %}{{ t }}{{ ", " if not loop.last }}{%- endfor %}
{% endif %}

{{NEWLINE}}

{%- if cask -%}
- homecask_cask:
  name: caskroom/versions/java8, {% for c in cask %}{{ c }}{{ ", " if not loop.last }}{%- endfor %}
{% endif %}

{{NEWLINE}}

{%- if brew -%}
- homebrew:
  name: {% for b in brew %}{{ b }}{{ ", " if not loop.last }}{%- endfor %}
{% endif %}

{{NEWLINE}}

{%- if mas -%}
# FIXME: dictionary
#- homebrew_mas:
#  name: {% for m in mas %}{{ m }}{{ ", " if not loop.last }}{%- endfor %}
{% endif -%}
'''

TPL_STR2 = '''{#- jinja2 -#}
{%- set NEWLINE='\n' -%}
# Don't edit, this.  Edit list.yml and run ./main.py to generate this.
---

{% if tap %}
{% for t in tap %}
- name: Install tap {{t}}
  homebrew_tap:
    name: {{t}}
{%- endfor %}

{{NEWLINE}}
{% endif %}

{% if cask %}
{% for c in cask %}
- name: Install cask {{c}}
  homebrew_cask:
    name: {{c}}
{%- endfor %}

{{NEWLINE}}
{% endif %}

{% if brew %}
{% for b in brew %}
- name: Install brew {{b}}
  homebrew:
    name: {{b}}
{%- endfor %}

{{NEWLINE}}
{% endif %}

{% if mas %}
# FIXME: mas is dictionary
{% for m in mas %}
#- name: Install mas {{m}}
#  homebrew_mas:
#    name: {{m}}
{%- endfor %}

{{NEWLINE}}
{% endif %}
'''

tpl_ansible = jinja2.Template(TPL_STR1)
tpl_ansible = jinja2.Template(TPL_STR2)


def write_single_file(dct):
    with open(f'macos.yml', 'w') as macos:
        dct = {
            'brew': dct['brew'],
            'cask': dct['cask'],
            'tap': dct['tap'],
            'mas': dct['mas']}
        macos.write(tpl_ansible.render(dct))


def write_split_files(dct):
    brews = list(common.chunks(dct['brew'], MAX_PACKAGES_PER_GROUP // 2))
    cask = list(common.chunks(dct['cask'], MAX_PACKAGES_PER_GROUP // 2))
    # FIXME: add mas

    combined = list(zip_longest(brews, cask))

    for idx, lst in enumerate(combined):
        with open(f'macos{idx+1}.yml', 'w') as macos:
            dct = {
                'brew': combined[idx][0],
                'cask': combined[idx][1],
                'tap': dct['tap'],
                'mas': dct['mas']}
            tplr = tpl_ansible.render(dct)
            macos.write(tplr)


def create_taskfiles(dct):
    write_single_file(dct)
    write_split_files(dct)
