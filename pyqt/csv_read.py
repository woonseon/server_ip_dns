#-*-coding:utf-8-*-

import sys
import csv
#pip3 install PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_UI()

    def setup_UI(self):
        # set up window size
        self.setGeometry(500, 100, 800, 500)
        self.setWindowTitle("csv viewer")

        # set Table
        self.tableWidget = QTableWidget(self)
        
        # set Column
        self.tableWidget.setColumnCount(4)
        # self.tableWidget.setHorizontalHeaderLabels(['Time', 'Address', 'ip', 'dns'])
        self.colum_setting()
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

        # open button, close button
        self.btn_open = QPushButton("파일 열기", self)
        self.btn_open.clicked.connect(self.file_open)
        
        self.btn_close = QPushButton("창닫기", self)
        self.btn_close.clicked.connect(QCoreApplication.instance().quit)

        # mal ip print
        self.btn_sort = QPushButton("악의적인 ip 출력", self)
        self.btn_sort.clicked.connect(self.find_mal_ip)

        # mal ip print
        self.text_ip = QLineEdit("악의적인 ip 입력: ", self)
        self.text_ip.returnPressed.connect(self.text_ip_changed)


        self.btn_action = QPushButton("악의적인 ip 행위 출력", self)
        self.btn_action.clicked.connect(self.find_mal_ip_action)

        # csv 저장
        self.btn_out_csv = QPushButton("csv로 저장", self)
        self.btn_out_csv.clicked.connect(self.out_csv)

        # layout
        high_LayOut = QHBoxLayout()
        high_LayOut.addWidget(self.btn_open)
        high_LayOut.addWidget(self.btn_close)

        midium_LayOut = QHBoxLayout()
        midium_LayOut.addWidget(self.btn_sort)
        midium_LayOut.addWidget(self.text_ip)
        midium_LayOut.addWidget(self.btn_action)
        midium_LayOut.addWidget(self.btn_out_csv)

        low_LayOut = QVBoxLayout()
        low_LayOut.addWidget(self.tableWidget)
        self.tableWidget.setColumnWidth(0, 220)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 203)
        self.tableWidget.setColumnWidth(3, 130)
        
        layout = QVBoxLayout()
        layout.addLayout(high_LayOut)
        layout.addLayout(low_LayOut)
        layout.addLayout(midium_LayOut)

        self.setLayout(layout)

    def file_open(self):
        files = QFileDialog.getOpenFileNames(self)
        for f in files[0]:
            file_name = f.split('/')[-1]
            file_path = f
            if (".csv" in file_name):
                self.line_list = []
                self.ip = []
                
                f_csv = open(file_name, 'r', encoding='utf-8')
                rdr = csv.reader(f_csv)
                for line in rdr:
                    row_numb = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row_numb)
                    i = (int(line[0])-1)
                    # csv list input          
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(line[1]))
                    self.tableWidget.setItem(i, 1, QTableWidgetItem(line[2]))
                    self.tableWidget.setItem(i, 2, QTableWidgetItem(line[3]))
                    self.tableWidget.setItem(i, 3, QTableWidgetItem(line[4]))
      
                    self.ip.append(line[3])
                    self.line_list.append(line)

                f_csv.close()

            else:
                QMessageBox.about(self, "Warning", "This is not csv file")
    
    def colum_setting(self):
        self.tableWidget.setHorizontalHeaderLabels(['Time', 'Address', 'ip', 'dns'])
    
    def find_mal_ip(self):
        QMessageBox.about(self, "Malicious ip", "\n".join(set(self.ip)))
    
    def find_mal_ip_action(self):
        self.tableWidget.clear()
        self.colum_setting()
        self.mali_ip = set(self.ip)
        row_number = 0

        for i in range(len(self.line_list)-1):
            if(self.line_list[i][3] in (list(self.mali_ip)[1])):
                #print(self.line_list[i])
                row_numb = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_numb)
                self.tableWidget.setItem(row_number, 0, QTableWidgetItem(self.line_list[i][1]))
                self.tableWidget.setItem(row_number, 1, QTableWidgetItem(self.line_list[i][2]))
                self.tableWidget.setItem(row_number, 2, QTableWidgetItem(self.line_list[i][3]))
                self.tableWidget.setItem(row_number, 3, QTableWidgetItem(self.line_list[i][4]))
                row_number += 1
            
    def out_csv(self):
        f_csv = open('malicious_action.csv', 'w', encoding='utf-8')
    
    def text_ip_changed(self):
        print(self.showMessage(self.lineEdit.text()))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()