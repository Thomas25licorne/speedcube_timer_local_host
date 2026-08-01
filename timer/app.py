import sys
from PyQt6.QtWidgets import QApplication
from UI import SpeedcubeTimer 
#from ui_window_mulitple_sessions import SpeedcubeTimer

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SpeedcubeTimer()
    window.show()
    sys.exit(app.exec())