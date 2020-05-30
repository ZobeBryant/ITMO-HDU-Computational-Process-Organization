import fz_cli as fz_cli

class Example(object):
  """A simple calculator class."""

  def double(self, number):
    return 10 * number

if __name__ == '__main__':
  fz_cli.Fz(Example)

# def hello(name="World"):
#   return "Hello %s!" % name
#
# if __name__ == '__main__':
#     fz_cli.Fz(hello)

