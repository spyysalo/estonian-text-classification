#!/usr/bin/env python3

import sys

from sklearn.model_selection import train_test_split


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('--seed', default=None, type=int)
    ap.add_argument('train', type=float)
    ap.add_argument('dev', type=float)
    ap.add_argument('test', type=float)
    ap.add_argument('file')
    ap.add_argument('train_out')
    ap.add_argument('dev_out')
    ap.add_argument('test_out')
    return ap


def get_labels(data):
    labels = []
    for fields in data:
        labels.append('/'.join([fields[0], fields[3]]))
    return labels


def main(argv):
    args = argparser().parse_args(argv[1:])
    if args.train + args.dev + args.test != 1.0:
        raise ValueError('Ratios do not add up to 1.0')
    data = []
    with open(args.file) as f:
        for ln, l in enumerate(f, start=1):
            l = l.rstrip('\n')
            data.append(l.split('\t'))
    labels = get_labels(data)
    train, rest = train_test_split(data, train_size=args.train,
                                   stratify=labels, random_state=args.seed)
    rest_labels = get_labels(rest)
    dev_ratio = args.dev/(args.dev+args.test)
    dev, test = train_test_split(rest, train_size=dev_ratio,
                                 stratify=rest_labels, random_state=args.seed)
    for fn, subset in ((args.train_out, train),
                       (args.dev_out, dev),
                       (args.test_out, test)):
        with open(fn, 'w') as out:
            for fields in subset:
                print('\t'.join(fields), file=out)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
