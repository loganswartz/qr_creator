#!/usr/bin/env python3

# builtins
import pathlib

# 3rd party
from PySide2.QtWidgets import (
    QVBoxLayout, QFrame, QSizePolicy, QGridLayout, QWidget, QLineEdit, QLabel,
    QCheckBox, QPushButton, QFileDialog, QPlainTextEdit
)
from PySide2.QtGui import QPixmap, QColor, QFont, QFontMetrics
from PySide2.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("QR Creator")

        # data input
        self.data = QLineEdit()
        self.data.setPlaceholderText("Data to encode...")

        # QR preview
        self.preview = QLivePreview(parent=self)

        # generate button
        self.generate = QPushButton("Generate && Save")   # '&' is interpreted by PySide, see docs
        self.generate.setDefault(True)

        # output filebrowsing controls
        self.file_browse = QFileBrowse(parent=self)

        # window layout
        layout = QVBoxLayout()
        layout.setSizeConstraint(layout.SetFixedSize)
        layout.addWidget(self.preview)
        layout.addWidget(self.data)
        layout.addWidget(self.file_browse)
        layout.addWidget(self.generate)

        self.setLayout(layout)

    @property
    def submit_func(self):
        return self._submit_func or None

    @submit_func.setter
    def submit_func(self, func):
        self._submit_func = func
        self.data.returnPressed.connect(lambda: self._submit_func(self))
        self.generate.clicked.connect(lambda: self._submit_func(self))


class QLivePreview(QWidget):
    """
    A custom class that can show an empty canvas with a message, or an image without a message.
    """
    def __init__(self, placeholder: str = '(Nothing to preview)', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = QLabel()
        self.window.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.window.setLineWidth(2)

        self.placeholder_text = QLabel(parent=self.window)
        self.placeholder_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.placeholder_text.setAlignment(Qt.AlignCenter)
        self.placeholder_text.setText(placeholder)

        # placeholder background when nothing is shown
        self.blank_background = QPixmap(290, 290)
        self.blank_background.fill(QColor(0, 0, 0, 32))

        self.preview_layout = QVBoxLayout()
        self.preview_layout.addWidget(self.placeholder_text)
        # self.window.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.window.setLayout(self.preview_layout)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.window)
        self.setLayout(self.layout)

        self.clearImage()

    def clearImage(self):
        self.window.setPixmap(self.blank_background)
        self.placeholder_text.show()

    def setImage(self, image: QPixmap):
        self.placeholder_text.hide()
        self.window.setPixmap(image)


class QFileBrowse(QWidget):
    def __init__(self, subfolder_name='QR Codes', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QGridLayout()
        self.button = QPushButton("Change save location")
        self.subfolder = QCheckBox("Create subfolder")
        self.subfolder.stateChanged.connect(self.update_display)
        self.button.clicked.connect(self.browse)
        self.subfolder_name = subfolder_name
        self.dialog = QFileDialog()
        self._base_path = pathlib.Path(".").expanduser().resolve()

        # output path display
        self.path_display = QPlainTextEdit()
        # make bold
        font = self.path_display.font()
        font.setWeight(QFont.Bold)
        self.path_display.setFont(font)
        # configure height
        self.path_display.setFixedHeight(QFontMetrics(font).height() * 2)
        self.path_display.setLineWrapMode(QPlainTextEdit.NoWrap)
        # styles
        self.path_display.setReadOnly(True)
        self.path_display.setFrameStyle(QFrame.Box | QFrame.Sunken)
        self.path_display.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.path_display.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        self.path_display.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.path_display.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # add widgets to layout
        self.layout.addWidget(self.button, 0, 0)
        self.layout.addWidget(self.subfolder, 0, 1)
        self.layout.addWidget(self.path_display, 1, 0, 1, 2)
        self.layout.setMargin(0)

        self.setLayout(self.layout)
        self.update_display()

    @property
    def save_path(self):
        if self.subfolder.isChecked():
            return self._base_path / self.subfolder_name
        return self._base_path

    def browse(self):
        path = self.dialog.getExistingDirectory()
        if path != '':
            self._base_path = pathlib.Path(path).expanduser().resolve()
        self.update_display()

    def update_display(self):
        scrollbar = self.path_display.horizontalScrollBar()
        old_scroll = scrollbar.value()
        scrolled_to_end = old_scroll == scrollbar.maximum()

        self.path_display.setPlainText(str(self.save_path))

        if scrolled_to_end:
            scrollbar.setValue(scrollbar.maximum())
        else:
            scrollbar.setValue(old_scroll)

