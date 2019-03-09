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
- echo SOMEVAR="$SOMEVAR"

osx_image:
- xcode10.1

env:
{%- for count in range(1,COUNT+1): %}
- BREWFILE=Brewfile{{ count }}
{%- endfor %}
global:
  secure: DvR+f01wOdJb5sH53650HWzz7dYy2wkV/PzgdVtVPwsXP3QOO6IT72C0YJqTZho+HbbjtX3uCUuN40HH5E/v4kl5uSEkrCUmBuMImkQyK+ffbSZevT+JKUX9nHHwpL+SlkuuBAHgcYrusYTXnnsujSVtotvbOFhJidNIzsJtphyMG7mJgO90iESVr50YeFx6HIFWIJ/9gxD2SDw0SRphk97jxtqLV0eIwyKKHxPfU6UxN1FF1dmKmMV2LHOfMZkjT7agCjgxqoIbvng6o5AsMClx9qa6iATdeQE41YMG5PYqxJoS+AmcH9VGGHiFsct9ydzLkI74BSFUQV9anzmTfz8JLFwPYbH8WfmWgXIqfPnuwx/lkHH12c+qTiov2+3NYVm482JZ26RnhV9HLxIHyTD53e0Oa0aa4XqR6HB5FQ7Y/Vzl7t1L6PqvY3UOZY6n/4OOrme20YuGT2hvKnQawG23l9OEzrstjXWwZ7WhdBewHznzNagKZDLsMDTii6A8jMptVc2FF6UGhAsSe0yANNngs+QuwRDwAfnFJMmhr0O5La61s9Zq2mjLXrz4iqWXa/Long8kiC00gqiyvGumOdriZSAntvd7VVB9ddg5rZtA4YupkzKGl3RDfO+zLR0bZCNyEEpsl/yWM9atVIB+ej6HHgX/9qNPtd1bE0fdKAQ=

script:
- travis_retry brew bundle --file=test/$BREWFILE --verbose
""")


tpl_brewfile = Template("""{#- jinja2 -#}
tap "caskroom/versions"
{% for tap in data.taps -%}
{{ tap }}
{%- endfor %}

cask "java8"
{% for item in data.casks_brews_mas -%}
{{ item }}
{%- endfor %}
""")


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def add_to_bucket(line):
    re.match(r'^(tap +"([^\"]+)".*)', line) and taps.append(line)
    re.match(r'^(cask +"([^\"]+)".*)', line) and casks.append(line)
    re.match(r'^(brew +"([^\"]+)".*)', line) and brews.append(line)
    re.match(r'^(mas +"([^\"]+)".*)', line) and mas.append(line)


brews = []
casks = []
taps = []
mas = []


def main():

    with open('../Brewfile', 'r') as brewfile:
        for line in brewfile.readlines():
            add_to_bucket(line)

    data = {}
    data['taps'] = taps
    all = brews + casks + mas
    TOTAL_SPLITS = 0

    for chunk in list(chunks(all, COUNT)):
        TOTAL_SPLITS += 1
        with open('Brewfile{}'.format(TOTAL_SPLITS), 'w') as brewfile:
            data['casks_brews_mas'] = chunk
            brewfile.write(tpl_brewfile.render(data=data))

    with open('.travis.yml', 'w') as travis:
        travis.write(tpl_travis.render(COUNT=TOTAL_SPLITS))


if __name__ == "__main__":
    # execute only if run as a script
    main()
