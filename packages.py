import os
import pprint
import tempfile
from dataclasses import dataclass
from itertools import zip_longest
from typing import List

try:
    from yaml import CLoader as Loader, load, dump
except ImportError:
    from yaml import Loader, load, dump

MAX_PACKAGES_PER_GROUP = 10


@dataclass
class PackageStore:
    """Class for keeping track of hombrew brews, casks, mas, etc."""
    brews: List[str] = None
    casks: List[str] = None
    taps: List[str] = None
    mas: List[str] = None
    fields: List[str] = None
    data_fname: str = None
    pairs: List = None

    def __post_init__(self):
        self.data_fname = 'list.yml'
        self.fields = ['brews', 'casks', 'taps', 'mas']
        dct = load(open(self.data_fname), Loader=Loader)
        for field in self.fields:
            setattr(self, field, dct[field])
        self.pairs = self.create_pairs()
        self.clean_yaml()

    def clean_yaml(self):
        fd, path = tempfile.mkstemp()
        f = os.fdopen(fd, 'w')
        d = {}
        for pkgtype in self.fields:
            x = getattr(self, pkgtype)
            try:
                y = set(x)  # FIXME: fails for mas which is dict
                z = sorted(y)
            except TypeError:
                z = x
            d[pkgtype] = z
        f.write(dump(d, default_flow_style=False))
        f.flush()
        os.rename(path, self.data_fname)

    def create_pairs(self):
        brews = list(chunks(self.brews, MAX_PACKAGES_PER_GROUP // 2))
        casks = list(chunks(self.casks, MAX_PACKAGES_PER_GROUP // 2))
        # FIXME: add mas

        return list(zip_longest(brews, casks))

    def get_map(self):
        d = {}
        for pkgtype in self.fields:
            d[pkgtype] = getattr(self, pkgtype)
        return d

    def write_single_file(self, basename, template):
        target = basename.format('')
        with open(target, 'w') as fh:
            fh.write(template.render(self.get_map()))

    def split_targets(self, basename):
        d = []
        for idx, lst in enumerate(self.pairs):
            d.append(basename.format(idx + 1))

        return d

    def write_split_files(self, basename, template):
        d = self.split_targets(basename)
        for idx, lst in enumerate(self.pairs):
            target = d[idx]
            with open(target, 'w') as fh:
                dct = {
                    'brews': self.pairs[idx][0],
                    'casks': self.pairs[idx][1],
                    'taps': self.taps,
                    'mas': self.mas}
                tplr = template.render(dct)
                fh.write(tplr)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def main():
    ps = PackageStore()
    pprint.pprint(ps.brews)


if __name__ == "__main__":
    main()
