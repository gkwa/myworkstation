import re
from pprint import pprint

from jinja2 import Template

COUNT = 90

tpl_travis = Template("""{#- jinja2 -#}
language: ruby
cache: bundler

sudo: required
dist: trusty

group: edge
os: osx
before_install:
  - brew update

osx_image:
  - xcode10.1
  - xcode9.2

env:
{%- for count in range(1,COUNT+1): %}
  - BREWFILE=Brewfile{{ count }}
{%- endfor %}

script:
- travis_retry brew bundle --file=test/$BREWFILE --verbose
""")

tpl_brewfile = Template("""{#- jinja2 -#}
tap "caskroom/versions"
{% for tap in data.taps -%}
{{ tap }}
{%- endfor %}

cask "java8"
{% for bc in data.casks_brews -%}
{{ bc }}
{%- endfor %}
""")


brews = []
casks = []
taps = []
mas = []


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


with open('../Brewfile', 'r') as brewfile:
    for line in brewfile.readlines():
        line.strip()
        mo = re.match(r'^(tap +"([^\"]+)".*)', line)
        if mo:
            taps.append(line)
            continue

        mo = re.match(r'^(cask +"([^\"]+)".*)', line)
        if mo:
            casks.append(line)
            continue

        mo = re.match(r'^(brew +"([^\"]+)".*)', line)
        if mo:
            brews.append(line)
            continue

        mo = re.match(r'^(mas +"([^\"]+)".*)', line)
        if mo:
            mas.append(line)
            continue

data = {}
data['taps'] = taps
all = brews + casks
i = 0
TOTAL_SPLITS = 0

for c in list(chunks(all, COUNT)):
    i += 1
    TOTAL_SPLITS = i
    with open('Brewfile{}'.format(i), 'w') as brewfile:
        data['casks_brews'] = c
        brewfile.write(tpl_brewfile.render(data=data))

with open('../.travis.yml', 'w') as travis:
    travis.write(tpl_travis.render(COUNT=TOTAL_SPLITS))
