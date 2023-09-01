#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os

from mainwindow import MainWindow

from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    SAVE_PATH = "./music"
    if(not os.path.exists(SAVE_PATH)):
        os.mkdir(SAVE_PATH)

    app = QApplication(sys.argv)

    mainwindow = MainWindow()
    mainwindow.show()

    app.exec()