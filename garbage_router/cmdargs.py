import argparse
from functools import cache

parser = argparse.ArgumentParser()
parser.add_argument('input')
parser.add_argument('a', type=float, default=1.0)
parser.add_argument('b', type=float, default=1.0)

@cache
def args():
    return parser.parse_args()