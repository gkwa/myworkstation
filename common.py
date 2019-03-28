import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def load(path):
    dct = yaml.load(open(path), Loader=Loader)
    dct = clean(dct)

    with open('list.yml', 'w') as outfile:
        yaml.dump(dct, outfile, default_flow_style=False)

    return dct


def clean(dct):
    """
    remove duplicates
    :param dct:
    :return: dct
    """
    dct['brew'] = sorted(set(dct['brew']))
    dct['tap'] = sorted(set(dct['tap']))
    dct['cask'] = sorted(set(dct['cask']))
    dct['mas'] = dct['mas']  # FIXME: this is dictionary

    return dct


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
