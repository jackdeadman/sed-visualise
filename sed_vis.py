"""
Command line tool to work with the SED Visualise framework
"""

import sys
import path

from lib.generators.system_generator import SystemGenerator

args = sys.argv[1:]


def generate(mode, name):
    if mode == 'system':
        generator = SystemGenerator(name)

    generator.generate()

if args[0] == 'generate':
    generate(args[1], args[2])
