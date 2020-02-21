#!/usr/bin/env python3

import sys
import csv

from logging import warning


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('--dedup', default=False, action='store_true')
    ap.add_argument('file')
    return ap


def main(argv):
    args = argparser().parse_args(argv[1:])
    seen = set()
    with open(args.file) as f:
        for ln, l in enumerate(f, start=1):
            if l.isspace() or not l:
                continue
            l = l.rstrip('\n')
            fields = l.split(',', 4)
            data, text = fields[:4], fields[4]
            assert text.startswith('"') and text.endswith('"')
            text = text[1:-1].strip()
            alnum_text = ''.join(c for c in text if c.isalnum())
            if args.dedup and alnum_text in seen:
                warning('dedup: ignoring duplicate "{}"'.format(text))
                continue
            seen.add(alnum_text)
            print('\t'.join(data+[text]))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
