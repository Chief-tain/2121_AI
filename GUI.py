from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import os
from pathlib import Path, PurePath
import pandas as pd
from exif import Image
from datetime import datetime

from styles import button_style, text_box_style, table_style

from model import Prediction

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.prediction = Prediction()
        self.counter = 0

        self.names, self.results, self.models, self.dates, self.times = [], [], [], [], []

        self.setWindowTitle("Искусственный интеллект определяет лебедей")
        self.setFixedSize(1450, 900)
        self.setObjectName("MainWindow")
        # self.setStyleSheet("border-image:url(fon.jpg)")
        self.setStyleSheet("#MainWindow{border-image:url(fon2.png)}")
        # self.setWindowIcon(QIcon('14.jpg'))

        self.bt0 = QPushButton("Выбрать изображения", self)
        self.bt0.move(10, 10)
        self.bt0.setFont(QFont('San Francisco', 20))
        self.bt0.setFixedSize(300, 80)
        self.bt0.setObjectName("pushButton")
        self.bt0.setStyleSheet(button_style)
        self.bt0.clicked.connect(self.open_file_dialog)

        self.bt1 = QPushButton("Экспорт в Excel", self)
        self.bt1.move(10, 700)
        self.bt1.setFont(QFont('San Francisco', 20))
        self.bt1.setFixedSize(300, 80)
        self.bt1.setObjectName("pushButton")
        self.bt1.setStyleSheet(button_style)
        self.bt1.clicked.connect(self.excel)

        self.bt2 = QPushButton("Экспорт в CSV", self)
        self.bt2.move(10, 610)
        self.bt2.setFont(QFont('San Francisco', 20))
        self.bt2.setFixedSize(300, 80)
        self.bt2.setObjectName("pushButton")
        self.bt2.setStyleSheet(button_style)
        self.bt2.clicked.connect(self.csv)

        self.bt3 = QPushButton("Выбрать папку", self)
        self.bt3.move(10, 100)
        self.bt3.setFont(QFont('San Francisco', 20))
        self.bt3.setFixedSize(300, 80)
        self.bt3.setObjectName("pushButton")
        self.bt3.setStyleSheet(button_style)
        self.bt3.clicked.connect(self.open_folder)

        self.bt4 = QPushButton("Очистить данные", self)
        self.bt4.move(10, 190)
        self.bt4.setFont(QFont('San Francisco', 20))
        self.bt4.setFixedSize(300, 80)
        self.bt4.setObjectName("pushButton")
        self.bt4.setStyleSheet(button_style)
        self.bt4.clicked.connect(self.clean_data)

        # self.lbl = QLabel(self)
        # self.lbl.move(5, 5)
        # self.lbl.resize(200, 200)

        self.label = QLabel('<b>Распознано лебедей: 0</b>', self)
        self.label.setGeometry(10, 200, 500, 500)
        self.label.setFont(QFont('San Francisco', 14))
        self.label.setStyleSheet("color: white")

        self.label1 = QLabel('<b>Лебедь-шипун: 0</b>', self)
        self.label1.setGeometry(10, 225, 500, 500)
        self.label1.setFont(QFont('San Francisco', 14))
        self.label1.setStyleSheet("color: white")

        self.label2 = QLabel('<b>Лебедь-кликун: 0</b>', self)
        self.label2.setGeometry(10, 250, 500, 500)
        self.label2.setFont(QFont('San Francisco', 14))
        self.label2.setStyleSheet("color: white")

        self.label3 = QLabel('<b>Малый лебедь: 0</b>', self)
        self.label3.setGeometry(10, 275, 500, 500)
        self.label3.setFont(QFont('San Francisco', 14))
        self.label3.setStyleSheet("color: white")

        self.table = QTableWidget(self)  # Create a table
        self.table.setColumnCount(5)     #Set three columns
        self.table.setRowCount(1000)        # and one row
 
        # Set the table headers
        self.table.setHorizontalHeaderLabels(["Название изображения", "Результат распознавания", 'Дата и время распознавания', 'Модель камеры', 'Дата и время фото'])

        # Установить нередактируемый режим
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # Установите размер картинки
        # self.table.setIconSize(QSize(300 ,200))

        # self.table.setColumnWidth(3 , 300)
        # Размер ячеек в зависимости от размера таблицы
        header = self.table.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        strs = self.table.verticalHeader()
        strs.setSectionResizeMode(0, QHeaderView.Stretch)

        # Set the alignment to the headers
        for i in range(2):
            self.table.horizontalHeaderItem(i).setTextAlignment(Qt.AlignHCenter)
 
        # Do the resize of the columns by content
        self.table.resizeColumnsToContents()
        self.table.setGeometry(350, 10, 1080, 770)
        self.table.cellClicked.connect(self.cell_was_clicked)
        self.table.setStyleSheet("QTableWidget {background-color: rgba(255,255,255,200);}")

        # item = QTableWidgetItem()
        # self.table.setItem(0, 0, item)
        # item.setIcon(QIcon("img_0.jpg"))
        # self.table.setIconSize(QSize(100, 100))

        self.show()
    
    def get_extra_info(self, filename):
        self.extra_info = []
        try:
            with open(filename, "rb") as file:
                image = Image(file)
                try:
                    self.extra_info.append(image.model)
                except:
                    self.extra_info.append('')

                try:
                    self.extra_info.append(image.datetime_original)
                except:
                    self.extra_info.append('')

                # print(self.extra_info)
        except:
            self.extra_info = ['', '']


    def cell_was_clicked(self, row, column):
        try:
            item = self.table.item(row, column).text()
            os.startfile(item)
        except FileNotFoundError:
            pass

        self.get_extra_info(item)

    def get_file_name(self,file_dir):    # Получить файлы в указанную папку
        '''
                 Получить все имена файлов в указанном каталоге
                 : param file_dir: указать каталог
                 : return: вернуть список имен файлов
        '''
        for root, dirs, files in os.walk(file_dir):
            # return root # Текущий путь к каталогу
            # return dirs # Все подкаталоги по текущему пути
            return files  # Все субфайлы вне каталога в текущем пути

    def open_folder(self):
         
        # '. /' указывает текущий путь
        path = QFileDialog.getExistingDirectory(self, 'Выбрать файл', './')
        # Поле метки отображает текстовый путь
        data = self.get_file_name(path)
        for i in range(len(data)):
            if str(data[i]).endswith('.jpg') or str(data[i]).endswith('.png'):

                self.prediction.predict(str(data[i]))

                self.names.append(str(data[i]))
                self.results.append(self.prediction.res)

                self.get_extra_info(str(data[i]))
                self.models.append(self.extra_info[0])
                self.dates.append(self.extra_info[1])
                self.times.append(f"{datetime.now()}"[:19])

        for i in range(self.counter, len(self.results)):
            self.table.setItem(self.counter, 0, QTableWidgetItem(f"{self.names[i]}"))
            self.table.setItem(self.counter, 1, QTableWidgetItem(f"{self.results[i]}"))
            self.table.setItem(self.counter, 2, QTableWidgetItem(self.times[i]))
            self.table.setItem(self.counter, 3, QTableWidgetItem(f"{self.models[i]}"))
            self.table.setItem(self.counter, 4, QTableWidgetItem(f"{self.dates[i]}"))

            if self.results[i] == 'Малый лебедь':
                    for j in range(self.table.columnCount()):
                        self.table.item(i, j).setBackground(QBrush(QColor(242, 172, 65)))

            self.counter += 1

        self.update_labels(self.counter, self.results.count('Лебедь-шипун'), self.results.count('Лебедь-кликун'), self.results.count('Малый лебедь'))

    def open_file_dialog(self):

        filenames, ok = QFileDialog.getOpenFileNames(
            self,
            "Select a File", 
            "D:\\icons\\avatar\\", 
            "Images (*.png *.jpg)"
        )
        if filenames:
            for filename in filenames:
                name = os.path.basename(filename)
                self.prediction.predict(name)

                self.names.append(name)
                self.results.append(self.prediction.res)

                self.get_extra_info(str(name))
                self.models.append(self.extra_info[0])
                self.dates.append(self.extra_info[1])
                self.times.append(f"{datetime.now()}"[:19])                

        for i in range(self.counter, len(self.results)):
            self.table.setItem(self.counter, 0, QTableWidgetItem(f"{self.names[i]}"))
            self.table.setItem(self.counter, 1, QTableWidgetItem(f"{self.results[i]}"))
            self.table.setItem(self.counter, 2, QTableWidgetItem(self.times[i]))
            self.table.setItem(self.counter, 3, QTableWidgetItem(f"{self.models[i]}"))
            self.table.setItem(self.counter, 4, QTableWidgetItem(f"{self.dates[i]}"))

            if self.results[i] == 'Малый лебедь':
                for j in range(self.table.columnCount()):
                    self.table.item(i, j).setBackground(QBrush(QColor(242, 172, 65)))

            self.counter += 1

        self.update_labels(self.counter, self.results.count('Лебедь-шипун'), self.results.count('Лебедь-кликун'), self.results.count('Малый лебедь'))

    def update_labels(self, tot, sh, kl, ml):
        self.label.setText(f'<b>Распознано лебедей: {tot}</b>')
        self.label1.setText(f'<b>Лебедь-шипун: {sh}</b>')
        self.label2.setText(f'<b>Лебедь-кликун: {kl}</b>')
        self.label3.setText(f'<b>Малый лебедь: {ml}</b>')

    def excel(self):
        df1 = pd.DataFrame({'Название изображения': self.names, 
                            'Результат распознавания': self.results,
                            'Дата и время распознавания': self.times,
                            'Модель камеры': self.models,
                            'Дата и время фото': self.dates})
        
        df1.to_excel("output.xlsx")  
        os.startfile('output.xlsx')

    def csv(self):
        df1 = pd.DataFrame({'Название изображения': self.names, 
                            'Результат распознавания': self.results,
                            'Дата и время распознавания': self.times,
                            'Модель камеры': self.models,
                            'Дата и время фото': self.dates})
        
        df1.to_csv("output.csv", index=False)
        os.startfile('output.csv')

    def clean_data(self):

        for i in range(len(self.results)):
            for j in range(self.table.columnCount()):
                self.table.setItem(i, j, QTableWidgetItem(''))

        self.counter = 0
        self.names, self.results, self.models, self.dates, self.times = [], [], [], [], []


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
    
