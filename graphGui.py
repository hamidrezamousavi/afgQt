from pyqtgraph import(
    PlotWidget,
   # Plot,
    mkPen
)
#class mPlot(Plot):
#    def __init__(self):
#        super().__init__()
#    def mouseHoverEvent(self):
#        print('test')

class Graph(PlotWidget):
    def __init__(self):
        super().__init__()
        self.forces =[0]
        self.sample_numbers=[0] 
        self.unit = ''
        self.pen = mkPen(width=1, color=(255,0,0))
        self.line = self.plot(pen = self.pen)
        self.showGrid(x=True, y=True)
        
    def update(self, unit, force, sample_number):
        self.sample_numbers.append(sample_number)
        self.forces.append(force)
        self.line.setData( self.sample_numbers, self.forces )

    def refresh_line(self):
        self.sample_numbers = []
        self.forces = []
        self.line.setData(self.sample_numbers,self.forces)
    