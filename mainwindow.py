#!/usr/bin/python
# -*- coding:utf-8 -*-

import re

from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QCheckBox
from PySide6.QtCore import Slot

from ui.mainwindow_ui import Ui_Widget

from downloader import search_music, download_music

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        
        self.ui.pushButton_search.clicked.connect(self.slot_pushButton_search_click)
        self.ui.pushButton_download.clicked.connect(self.slot_pushButton_download_click)
        self.ui.tableWidget_search_result.setSelectionBehavior(QTableWidget.SelectRows)

    def slot_pushButton_search_click(self):
        search_str = self.ui.lineEdit_search.text()

        search_ret = search_music(search_str)

        if(search_ret):
            self.ui.tableWidget_search_result.setRowCount(len(search_ret))
            for i in range(0, len(search_ret)):
                item_title = QTableWidgetItem(search_ret[i]["title"])
                item_url = QTableWidgetItem(search_ret[i]["url"])
                
                self.ui.tableWidget_search_result.setItem(i, 0, item_title)
                self.ui.tableWidget_search_result.setItem(i, 1, item_url)
                
    def slot_pushButton_download_click(self):
        items = self.ui.tableWidget_search_result.selectedItems()

        if(len(items) > 0):
            for i in range(1, len(items), 2):
                url = items[i].text()
                if(re.match(r"https://www.hifini.com/thread-\d+.htm", url)):
                    download_music(url, "./music/")