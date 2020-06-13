import unittest
from src.lab3.fz_cli import *


import os


class TestLab3(unittest.TestCase):
    #test support of flags with default values
    def test_default_values(self):
        cmd1 = 'python fz_cli.py -v'
        cmd2 = 'python fz_cli.py --version'
        cmd3 = 'python fz_cli.py -v --help'
        cmd4 = 'python fz_cli.py -v -h'
        res = os.popen(cmd1)
        output_str = res.read()
        self.assertEqual(output_str, "fz_cli_1.0.0\n")
        res = os.popen(cmd2)
        output_str = res.read()
        self.assertEqual(output_str, "fz_cli_1.0.0\n")
        res = os.popen(cmd3)
        output_str = res.read()
        self.assertEqual(output_str, "python version\n")
        res = os.popen(cmd4)
        output_str = res.read()
        self.assertEqual(output_str, "python version\n")


    def test_position_arguments(self):
        cmd1 = 'python fz_cli.py --cat _ example.txt'
        cmd2 = 'python fz_cli.py -c _ example.txt'
        cmd3 = 'python fz_cli.py --cat -h _'
        cmd4 = 'python fz_cli.py --cat --help _'
        res = os.popen(cmd1)
        output_str = res.read()
        self.assertEqual(output_str, 'Hello,this is fz_cli!\n')
        res = os.popen(cmd2)
        output_str = res.read()
        self.assertEqual(output_str, 'Hello,this is fz_cli!\n')
        res = os.popen(cmd3)
        output_str = res.read()
        self.assertEqual(output_str, 'read file\n')
        res = os.popen(cmd4)
        output_str = res.read()
        self.assertEqual(output_str, 'read file\n')

        # test named arguments with default values

    def test_named_arguments(self):
        cmd1 = 'python fz_cli.py --module _ get_version'
        cmd2 = 'python fz_cli.py -m _ get_library_description'
        res = os.popen(cmd1)
        output_str = res.read()
        self.assertEqual(output_str, 'The version of cli is fz_cli_1.0.0.\n')
        res = os.popen(cmd2)
        output_str = res.read()
        self.assertEqual(output_str, 'This is a simple command line interface library.\n')

    def test_sub_commands(self):
        cmd1 = 'python fz_cli.py --info _ lab'
        cmd2 = 'python fz_cli.py --info _ lab,variant'
        cmd3 = 'python fz_cli.py --info _ lab,variant,author'
        res = os.popen(cmd1)
        output_str = res.read()
        self.assertEqual(output_str, 'This is for lab3.\n')
        res = os.popen(cmd2)
        output_str = res.read()
        self.assertEqual(output_str, 'This is for lab3.\nOur variant is "Command line interface builder".\n')
        res = os.popen(cmd3)
        output_str = res.read()
        self.assertEqual(output_str, 'This is for lab3.\nOur variant is "Command line interface builder".\nThis is made by Zhao Qingbiao and Fan Xunlin.\n')

    def test_conversation(self):

        cmd1 = 'python fz_cli.py --conversation _ 1234'

        res = os.popen(cmd1)
        output_str = res.read()
        self.assertEqual(output_str, '{}\n'.format(1234))
