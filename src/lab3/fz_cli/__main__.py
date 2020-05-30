

import importlib
import sys

import fz_cli


def main(args):
  module_name = args[1]
  module = importlib.import_module(module_name)
  fz_cli.Fz(module, name=module_name, command=args[2:])


if __name__ == '__main__':
  main(sys.argv)
