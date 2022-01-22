import argparse
from functools import cache

parser = argparse.ArgumentParser()
parser.add_argument('input')
parser.add_argument('output')
parser.add_argument('a', type=float)
parser.add_argument('b', type=float)

@cache
def args():
    return parser.parse_args()