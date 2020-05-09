#!/usr/bin/env python3

# builtins
import pathlib
import sys
from typing import Any, NamedTuple
import argparse

# 3rd party
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QImage

# this module
from qr_creator.view import MainWindow
from qr_creator.model import make_qr, save_qr


def process_gui(ui, args):
    class QR(NamedTuple):
        data: Any
        image: QImage

    if ui.data.text() == '':
        return   # ignore empty inputs

    codes = [QR(item.strip(), make_qr(item.strip())) for item in ui.data.text().split(',')]
    if not ui.file_browse.save_path.exists():
        if not args.debug: ui.file_browse.save_path.mkdir()
    for (data, image) in codes:
        if not args.debug: save_qr(image, data, ui.file_browse.save_path)

    # update UI
    ui.preview.setImage(codes[-1].image)
    ui.data.clear()


def process_batch(args):
    data = [item.strip() for item in args.data.strip().split(',') if item.strip()]
    if len(data) == 0:
        print("No data given.")
        return
    print(f"Processing {len(data)} items....")
    for item in data:
        print(f"Generating QR for: {item}")
        if args.debug: continue   # skip if debugging
        save_qr(make_qr(item, pixmap = False), item, args.output)
    print("All QR codes saved.")


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-d', '--debug', help='Don\'t actually save QR codes to the disk', action='store_true')
#     parser.add_argument('-b', '--batch', help='Run the tool from the commandline. See additional info with the --help flag.', action='store_true')
#     parser.add_argument('-o', '--output', help='Path to the desired output directory', type=pathlib.Path, default='.')
#     parser.add_argument('data', help='Data to encode. May be a list separated by commas', nargs='?', default='')
#     args = parser.parse_args()
#
#     if args.batch:
#         process_batch(args)
#     else:
#         # init application
#         app = QApplication()
#         ui = MainWindow()
#
#         # connect ui
#         ui.submit_func = lambda ui: process_gui(ui, args)
#
#         # show and execute
#         ui.show()
#         sys.exit(app.exec_())
#
