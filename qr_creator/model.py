#!/usr/bin/env python3

# 3rd party
import qrcode
import PIL.ImageQt


def make_qr(data, pixmap=True):
    error_level = qrcode.constants.ERROR_CORRECT_H
    qr = qrcode.QRCode(error_correction=error_level, box_size=10)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    if pixmap:
        img = PIL.ImageQt.toqpixmap(img)
    return img


def save_qr(qr, filename, path):
    qr.save(str(path / str(filename + '.png')), 'PNG')

