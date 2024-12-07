from PyQt5.QtCore import (
    QObject,
    QRunnable,
    QThreadPool,
    QTimer,
    pyqtSignal,
    pyqtSlot,
)
import serial




class ReaderSignals(QObject):
    """
    Defines the signals available from a running worker thread.

    data
        tuple data point (unit, x, y)
    """

    data = pyqtSignal(tuple)  # <1>


class Reader(QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handle worker thread setup, signals
    and wrap-up.
    """

    def __init__(self):
        super().__init__()
        
        self.signals = ReaderSignals()
        self.forces = []
        self.samples = []
        self.unit = ''

    @pyqtSlot()
    def run(self):

        raw_data = []
        sample_number = 0
        self.ser = serial.Serial('COM1', 9600, timeout=0.1)
        self.do = True
        while self.do:
            temp = []
            unit = ''
            s = self.ser.read(1000)
            raw_data = s.decode('utf8','ignore').split()
            #convert data to float list   
            
            for item in raw_data:
                try:
                    temp.append(float(item))
                except ValueError:
                    unit = item if item in ['gf','kgf','N','ozf','lbf',] else unit
            try:
                mean = round(sum(temp)/len(temp), 2)
                sample_number += 1
            except ZeroDivisionError:
                continue
        
            self.forces.append(mean)
            self.samples.append(sample_number)
            self.unit = unit
            self.signals.data.emit((unit, mean, sample_number))
    def get_total_measurment(self):
        return ((self.unit, self.samples, self.forces))
    def close(self):
        self.do = False
        self.ser.close()
    
     

