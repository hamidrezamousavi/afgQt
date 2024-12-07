
from statistics import mean
from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QLabel,
    QGridLayout,
    QWidget,
    QLineEdit,

)
from PyQt5.QtCore import QThreadPool
from reader import ( Reader)
from graphGui import Graph

class StartButton(QPushButton):
    def __init__(self,label):
        super().__init__(label)
        self.setCheckable(True)
        self.setFixedSize(120,120)
        self.setStyleSheet("""
        border-radius :60 ;
        border : 2px solid black;
        background-color: rgb(64,64,64); 
        color: rgb(255,255,255);
        font-size:28px;
        font-family: 'Courier New';
        """)

class ForceAmountLabel(QLabel):
    def __init__(self,label):
        super().__init__(label)
        self.setFixedSize(200,70)
        self.setStyleSheet("""
        color: yellow;
        font-size:64px;
        font-family: 'Calibri (Body)';
        """)
class ForceUnitLabel(QLabel):
    def __init__(self, label):
        super().__init__(label)
        self.setStyleSheet("""
        color: rgb(10,255,10);
        font-size:36px;
        font-family: 'Courier New';
        """)
class CalculationLabel(QLabel):
    def __init__(self,label):
        super().__init__(label)
        self.setStyleSheet("""
        
        font-size:24px;
        font-family: 'Courier New';
        """)
class InputLine(QLineEdit):
    def __init__(self,*arg):
        super().__init__(*arg)
        self.setStyleSheet("""
        
        font-size:20px;
        font-family: 'Courier New';
        background: rgb(30,30,30);
        color: white;
        """)
class CalculationButton(QPushButton):
    def __init__(self,*arg):
        super().__init__(*arg)
        self.setStyleSheet("""
        
        font-size:20px;
        font-family: 'Courier New';
        background: rgb(50,50,50);
        color: white;

        """)

        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AFG")
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet("""
        background-color: black; 
        """)
        self.threadpool = QThreadPool()
        
        self.start_button = StartButton("START")
        self.start_button.clicked.connect(self.start_button_click)
        
        self.force_amount = ForceAmountLabel('     ')
        self.force_unit = ForceUnitLabel(' ')
        self.graph = Graph()
        self.row_range_label = CalculationLabel('From')
        self.lower_range = InputLine('10')
        self.upper_range_label = CalculationLabel('To')
        self.upper_range = InputLine('120')
        self.calculate_button = CalculationButton('Calculate')
        self.calculate_button.clicked.connect(self.calculate_button_click)
        self.min_label = CalculationLabel('Min')
        self.min_out = CalculationLabel(' 14.2 ')
        self.max_label = CalculationLabel('Max')
        self.max_out = CalculationLabel('18.9   ')
        
        self.mean_label = CalculationLabel('Mean')
        self.mean_out = CalculationLabel('16.3   ')
        
        self.layout = QGridLayout()
        
        self.layout.setContentsMargins(50,20,50,100)
        
       
        self.layout.addWidget(self.start_button,0,0)
        self.layout.addWidget(self.force_amount,1,0)
        
        self.layout.addWidget(self.force_unit,1,1)
        
        self.layout.addWidget(self.graph,1,3)
        
        self.layout.addWidget(self.row_range_label,3 ,0 )
        self.layout.addWidget(self.lower_range,4 ,0 )
        self.layout.addWidget(self.upper_range_label,5 ,0 )
        self.layout.addWidget(self.upper_range ,6 ,0 )
        self.layout.addWidget(self.calculate_button ,7 ,0 )
        self.layout.addWidget(self.min_label ,5 ,1 )
        self.layout.addWidget(self.min_out ,6 ,1 )
        self.layout.addWidget(self.max_label,5 ,2 )
        self.layout.addWidget(self.max_out ,6 ,2 )
        self.layout.addWidget(self.mean_label,5 ,3 )
        self.layout.addWidget(self.mean_out,6 ,3 )
       # self.layout.setAlignment(Qt.AlignLeft )
        self.w = QWidget()
        self.w.setLayout(self.layout)
        self.setCentralWidget(self.w)
    def start_button_click(self,e):
        if self.start_button.isChecked():
            self.graph.refresh_line()
            self.refresh_calculation()
            self.reader = Reader()
            self.reader.signals.data.connect(self.receive_data)
            self.threadpool.start(self.reader)
            self.start_button.setText('STOP')
        else:
            self.reader.close()
            self.unit, self.samples, self.forces = \
            self.reader.get_total_measurment()    
            self.start_button.setText('START')

    def receive_data(self, data):
        unit , force, sample_number = data 
        self.graph.update(unit, force, sample_number)
        self.force_amount.setText(str(force))
        self.force_unit.setText(unit)
        
        
    def calculate_button_click(self):
        low = int(self.lower_range.text())
        upper = int(self.upper_range.text())
        self.min_out.setText(str(min(self.forces[low:upper])))
        self.max_out.setText(str(max(self.forces[low:upper])))
        self.mean_out.setText(str(round(mean(self.forces[low:upper]),2)))
      
    def refresh_calculation(self):
        self.lower_range.setText('')
        self.upper_range.setText('')
        self.min_out.setText('')
        self.max_out.setText('')
        self.mean_out.setText('')


   

