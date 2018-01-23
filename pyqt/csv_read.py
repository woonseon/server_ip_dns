

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        # set up window size
        self.setGeometry(100, 500, 300, 300)
        self.setWindowTitle("csv viewer")
        self.resize(1080, 800)

        # set Table
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(20,90,600,665)
        
        self.tableWidget.setRowCount(100)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.setTableWidgetData()

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

        # open button, close button
        self.btn_open = QPushButton("열기", self)
        self.btn_open.move(20, 30)
        self.btn_open.clicked.connect(self.pushButtonClicked)
        
        self.btn_close = QPushButton("닫기", self)
        self.btn_close.move(120, 30)
        self.btn_close.clicked.connect(QCoreApplication.instance().quit)
    
    def setTableWidgetData(self):
        column_headers = ['Number', 'Time', 'Address', 'ip', 'dns']
        self.tableWidget.setHorizontalHeaderLabels(column_headers)

    def pushButtonClicked(self):
        files = QFileDialog.getOpenFileNames(self);
        for f in files[0]:
            file_name = f.split('/')[-1]
            file_path = f
            try:
                f = open(file_path, 'r')
                while True:
                    self.line = f.readline()
                    if not self.line: break

                    self.line_list = self.line.split(',')
                    print(self.line.split(','))

                    num_row = 0
                    self.csvTable.setItem(num_row, 3, QTableWidgetItem(str(self.line_list[2])))
                        
                f.close()

            except:
                self.errorbox = QMessageBox()
                self.errorbox.setText('This file is not csv File!!')
                # self.errorbox.exec()

    def closeWindow(self):
        window.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()