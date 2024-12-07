from PyQt5.QtWidgets import QApplication
from gui import MainWindow
import qtmodern.styles
import qtmodern.windows


app = QApplication([])
qtmodern.styles.dark(app)

window = qtmodern.windows.ModernWindow(MainWindow())
#window = MainWindow()
window.show()
app.exec_()