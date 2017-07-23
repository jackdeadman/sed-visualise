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

def remove(mode, name):
    if mode == 'system':
        generator = SystemGenerator(name)
    generator.remove()

if args[0] == 'generate':
    generate(args[1], args[2])

if args[0] == 'remove':
    remove(args[1], args[2])

if args[0] == 'regenerate':
    remove(args[1], args[2])
    generate(args[1], args[2])
