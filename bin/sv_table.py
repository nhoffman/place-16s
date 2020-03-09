#!/usr/bin/env python3
import sys
import argparse
import pandas
from collections import OrderedDict

RANKS = OrderedDict(
    [('k', 'kingdom'),
     ('p', 'phylum'),
     ('c', 'class'),
     ('o', 'order'),
     ('f', 'family'),
     ('g', 'genus'),
     ('s', 'species')]
)


def main(arguments):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    # inputs
    parser.add_argument('-c', '--classif', required=True)
    parser.add_argument('-s', '--specimens', required=True)
    parser.add_argument('-w', '--weights', required=True)
    # outputs
    parser.add_argument('--by-sv')          # 0
    parser.add_argument('--by-sv-long')     # 1
    parser.add_argument('--by-taxon')       # 2
    parser.add_argument('--by-taxon-rel')   # 3
    parser.add_argument('--by-taxon-long')  # 4
    parser.add_argument('--sv-names')       # 6
    args = parser.parse_args(arguments)
    dtype = {'name': str, 'rank': str, 'tax_name': str, 'likelihood': float}
    classif = pandas.read_csv(args.classif, dtype=dtype)
    weights = pandas.read_csv(
        args.weights,
        dtype={'name': str, 'sv': str, 'read_count': int},
        names=['name', 'sv', 'read_count'])
    specimens = pandas.read_csv(
        args.specimens,
        dtype=str,
        names=['sv', 'specimen'])
    classif = classif.merge(weights).merge(specimens)
    sv = classif.pivot_table(
        aggfunc='sum',
        index=['name', 'tax_name'],
        columns='specimen',
        fill_value=0,
        values='read_count')
    sv['total'] = sv[sv.columns].sum(axis='columns')
    sv = sv.sort_values(by='total', ascending=False)
    sv = sv.drop('total', axis='columns')
    sv.to_csv(args.by_sv, float_format='%.0f')
    sv_long = classif.sort_values(by='name')
    columns = ['specimen', 'name', 'rank', 'tax_name', 'read_count']
    sv_long.to_csv(args.by_sv_long, columns=columns, index=False)
    taxon = classif.pivot_table(
        aggfunc='sum',
        index='tax_name',
        columns='specimen',
        fill_value=0,
        values='read_count')
    taxon['total'] = taxon[sv.columns].sum(axis='columns')
    taxon = taxon.sort_values(by='total', ascending=False)
    taxon = taxon.drop('total', axis='columns')
    taxon.to_csv(args.by_taxon, float_format='%.0f')
    tl = classif.sort_values(by='tax_name')
    tl['total'] = tl.groupby(by='tax_name')['read_count'].transform('sum')
    tl.loc[:, 'read_count'] = tl['total']
    tl = tl[['specimen', 'tax_name', 'rank', 'read_count']]
    tl = tl.drop_duplicates()
    tl.to_csv(args.by_taxon_long, index=False)
    sv_names = classif['name'].sort_values().drop_duplicates()
    sv_names.to_csv(args.sv_names, index=False, header=False)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
