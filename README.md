# myworkstation
# Problems
## duplication
* you're storing the list too many times. You've loaded the list and
  then you've created pairs list and stored it in same object. This is
  bad.
* you're using generator in `chunks()`, but then you're storing this
  as a list in 'pairs' attribute so you gain nothing from using a
  generator.
## need filter for travis
* some casks/brews can't be installed like virtualbox on travis, need
  to add way to filter for travis
## keep comments
* if you comment out an item in `list.yml`, then you meant "I need to
  get back to this later", but now, commenting out an item means it
  will be removed because `yaml.load` respsects the comment and
  doesn't load it, but then when you write the yaml back to file then
  its removed.

  Is this an option: https://stackoverflow.com/a/27103244/1495086
