#-*-coding:utf-8-*-

import sys
import csv
import dns.resolver
import time
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
        self.setWindowTitle("Simple Viewer")

        # set Table
        self.table_Widget = QTableWidget(self)
        
        # set Column
        self.table_Widget.setColumnCount(4)
        self.colum_setting()
        self.table_Widget.resizeColumnsToContents()
        self.table_Widget.resizeRowsToContents()

        # nslookup
        self.title_1 = QLabel("Nslookup")
        self.lablName1 = QLabel("Main_DNS")
        self.editName1 = QLineEdit()
        self.lablName2 = QLabel("Sub_DNS")
        self.editName2 = QLineEdit()
        self.lablName3 = QLabel("Domain")
        self.editName3 = QLineEdit()
        self.btn_Ok = QPushButton("View ip")
        self.btn_Ok.clicked.connect(self.btnOk_Clicked)

        self.title_2 = QLabel("\nCsv Viewer")
        # open button, close button
        self.btn_open = QPushButton("파일 열기", self)
        self.btn_open.clicked.connect(self.file_open)
        
        self.btn_close = QPushButton("창닫기", self)
        self.btn_close.clicked.connect(QCoreApplication.instance().quit)

        # mal ip print
        self.btn_sort = QPushButton("ip 출력", self)
        self.btn_sort.clicked.connect(self.find_mal_ip)

        # 선택한 ip 출력
        self.lblName = QLabel("보고싶은 ip 입력")
        self.editName = QLineEdit()
        self.btnOk = QPushButton("OK")
        self.btnOk.clicked.connect(self.btnOkClicked)

        # layout
        title_layout = QHBoxLayout()
        title_layout.addWidget(self.title_1)

        title_layout2 = QHBoxLayout()
        title_layout2.addWidget(self.title_2)

        ip_layout = QHBoxLayout()
        ip_layout.addWidget(self.lablName1)
        ip_layout.addWidget(self.editName1)
        ip_layout.addWidget(self.lablName2)
        ip_layout.addWidget(self.editName2)
        ip_layout.addWidget(self.lablName3)
        ip_layout.addWidget(self.editName3)
        ip_layout.addWidget(self.btn_Ok)

        test_layout = QHBoxLayout()
        test_layout.addWidget(self.lblName)
        test_layout.addWidget(self.editName)
        test_layout.addWidget(self.btnOk)

        high_LayOut = QHBoxLayout()
        high_LayOut.addWidget(self.btn_open)
        high_LayOut.addWidget(self.btn_close)

        low_LayOut = QVBoxLayout()
        low_LayOut.addWidget(self.table_Widget)
        self.table_Widget.setColumnWidth(0, 220)
        self.table_Widget.setColumnWidth(1, 200)
        self.table_Widget.setColumnWidth(2, 203)
        self.table_Widget.setColumnWidth(3, 130)
        low_LayOut.addWidget(self.btn_sort)
        
        layout = QVBoxLayout()
        layout.addLayout(title_layout)
        layout.addLayout(ip_layout)
        layout.addLayout(title_layout2)
        layout.addLayout(low_LayOut)
        layout.addLayout(test_layout)
        layout.addLayout(high_LayOut)

        self.setLayout(layout)

    def file_open(self):
        self.table_Widget.clear()
        self.colum_setting()
        self.table_Widget.setRowCount(0)
        files = QFileDialog.getOpenFileNames(self)
        for f in files[0]:
            file_name = f.split('/')[-1]
            file_path = f
            if (".csv" in file_name):
                self.line_list = []
                self.ip = []
                
                f_csv = open(file_path, 'r', encoding='utf-8')
                rdr = csv.reader(f_csv)
                for line in rdr:
                    row_numb = self.table_Widget.rowCount()
                    self.table_Widget.insertRow(row_numb)
                    i = (int(line[0])-1)
                    # csv list input          
                    self.table_Widget.setItem(i, 0, QTableWidgetItem(line[1]))
                    self.table_Widget.setItem(i, 1, QTableWidgetItem(line[2]))
                    self.table_Widget.setItem(i, 2, QTableWidgetItem(line[3]))
                    self.table_Widget.setItem(i, 3, QTableWidgetItem(line[4]))
      
                    self.ip.append(line[3])
                    self.line_list.append(line)

                f_csv.close()

            else:
                QMessageBox.about(self, "Warning", "This is not csv file")
    
    def colum_setting(self):
        self.table_Widget.setHorizontalHeaderLabels(['Time', 'Address', 'ip', 'dns'])
    
    def find_mal_ip(self):
        try:
            QMessageBox.about(self, "Malicious ip", "\n".join(set(self.ip)))
        except:
            QMessageBox.about(self, "Warning", "Put file first")

    def btnOkClicked(self):
        try:
            input_ip = self.editName.text()
            self.table_Widget.clear()
            self.colum_setting()
            self.mali_ip = set(self.ip)
            row_number = 0
            add_list = []
            self.table_Widget.setRowCount(0)

            for index in range(len(self.line_list)):
                self.table_Widget.removeRow(index)            

            for i in range(len(self.line_list)):
                if(self.line_list[i][3] in (input_ip)):
                    add_list.append(self.line_list[i])

            for i in range(len(add_list)):
                row_numb = self.table_Widget.rowCount()
                self.table_Widget.insertRow(row_numb)
                self.table_Widget.setItem(row_number, 0, QTableWidgetItem(add_list[i][1]))
                self.table_Widget.setItem(row_number, 1, QTableWidgetItem(add_list[i][2]))
                self.table_Widget.setItem(row_number, 2, QTableWidgetItem(add_list[i][3]))
                self.table_Widget.setItem(row_number, 3, QTableWidgetItem(add_list[i][4]))
                row_number += 1
        except:
            QMessageBox.information(self, "Warning", "Input only ip")

    def btnOk_Clicked(self):
        try:
            main_dns = self.editName1.text()
            sub_dns = self.editName2.text()
            domain = self.editName3.text()
            domain = domain.replace('http://','')
            domain = domain.replace('https://','')
            self.table_Widget.clear()
            self.colum_setting()

            resolver = dns.resolver.Resolver()
            try:
                # main dns query
                resolver.nameservers = [main_dns]
                answers = resolver.query(domain)
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
                # sub dns query
                resolver.nameservers = [sub_dns]
                answers = resolver.query(domain)
                pass
            
            dns_address = []
            for rdata in answers:
                dns_address.append(rdata.address)
            
            QMessageBox.information(self, "Nslookup", str(domain) + "\n\n" + str("\n".join(set(dns_address))))
            
        except:
            QMessageBox.information(self, "Warning", "Input Correct please")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
