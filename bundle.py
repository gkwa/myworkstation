import jinja2

tpl_brewfile = jinja2.Template('''{#- jinja2 -#}
{% set NEWLINE='\n' -%}
# Don't edit, this.  Edit list.yml and run ./main.py to generate this.

{% if taps -%}
# taps
{% for tap in taps -%}
tap "{{ tap }}"
{% endfor %}
{%- endif -%}

{{NEWLINE}}

{%- if casks -%}
# cask
{% for cask in casks -%}
cask "{{ cask }}"
{% endfor %}
{%- endif -%}

{{NEWLINE}}

{%- if brews -%}
# brews
{% for brew in brews -%}
brew "{{ brew }}"
{% endfor %}
{%- endif -%}

{{NEWLINE}}

{%- if mas -%}
# mas
# FIXME: this is dictionary
{% for m in mas -%}
# mas "{{ mas }}"
{% endfor %}
{%- endif -%}
''')


def write_single_file(packages):
    rtpl = tpl_brewfile.render({
        'taps': packages['tap'],
        'casks': packages['cask'],
        'brews': packages['brew'],
        'mas': packages['mas']}
    )
    with open('Brewfile', 'w') as brewfile:
        brewfile.write(rtpl)


def create_brewfiles(packages):
    write_single_file(packages)
    # FIXME: not written yet
    # write_split_files(packages)
