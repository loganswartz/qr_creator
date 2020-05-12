#!/usr/bin/env python3

# builtins
import pathlib
import argparse
import sys

# 3rd party
from PySide2.QtWidgets import QApplication

# this module
from qr_creator.view import MainWindow
from qr_creator.controller import process_gui, process_batch


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', help='Don\'t actually save QR codes to the disk', action='store_true')
parser.add_argument('-b', '--batch', help='Run the tool from the commandline. See additional info with the --help flag.',
                    action='store_true')
parser.add_argument('-o', '--output', help='Path to the desired output directory', type=pathlib.Path, default='.')
parser.add_argument('data', help='Data to encode. May be a list separated by commas', nargs='?', default='')
args = parser.parse_args()


if args.batch:
    process_batch(args)
else:
    # init application
    app = QApplication()
    ui = MainWindow()

    # connect ui
    ui.submit_func = lambda ui: process_gui(ui, args)

    # show and execute
    ui.show()
    sys.exit(app.exec_())

