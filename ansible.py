from itertools import zip_longest

import jinja2

import common

MAX_PACKAGES_PER_GROUP = 60

TPL_STR = '''{#- jinja2 -#}
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

tpl_ansible = jinja2.Template(TPL_STR)


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
                'tap': dct['tap'], }
            tplr = tpl_ansible.render(dct)
            macos.write(tplr)


def create_taskfiles(dct):
    write_single_file(dct)
    write_split_files(dct)
