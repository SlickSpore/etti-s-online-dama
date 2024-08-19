from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QGridLayout, QMainWindow, QApplication, QWidget, QMenuBar
import sys

LIGHT_BROWN = "#ebd586"
DARK_BROWN  = "#4d3b2d"

class Dama(QMainWindow):
    def __init__(self):
        super(Dama, self).__init__()
        self.init_UserInterface()

    def squareClicked(self, x, y):
        print(f"Pressed {x, y}")

    def init_UserInterface(self):
        wid = QWidget(self)
        self.setCentralWidget(wid)
        grid_layout = QGridLayout()

        menubar = QMenuBar()
        menubar.addAction("View")
        grid_layout.addWidget(menubar)

        self.setGeometry(0,0,800,800)
        self.setWindowTitle("etti®'s online dama")

        for i in range(1, 9):
            for j in range(1, 9):
                button = QPushButton("")
                button.clicked.connect(lambda state, x = i, y = j: self.squareClicked(x, y))
                button.setStyleSheet(f"background-color : {DARK_BROWN if (j+i)%2 != 0 else LIGHT_BROWN}")
                button.setMinimumWidth(100)
                button.setMinimumHeight(100)
                grid_layout.addWidget(button, i, j)

        wid.setLayout(grid_layout)

def main():
    app = QApplication(sys.argv)
    win = Dama()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()