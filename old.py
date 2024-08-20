# includes

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QGridLayout, QMainWindow, QApplication, QWidget, QMenuBar, QMenu, QAction
import sys


# CONSTANTS
CLR_MODE = 0                # color theme
LIGHT_BROWN = "#ebd586"     # standard Light Color
DARK_BROWN = "#4d3b2d"      # standard Dark Color
HC_YELLOW = "#ffff00"       # High Contrast Light Color
HC_BLACK = "#000000"        # High Contrast Dark Color
W = 800
H = 800

# trigger function for each CheckerBoard Button
def squareClicked(x, y):
    print(f"Pressed {x, y}")

# shows the array of the checkerboard
def refresh_board(
        DARK=DARK_BROWN,
        LIGHT=LIGHT_BROWN,
        minimum_width=100,
        minimum_height=100,
        maximum_width=100,
        maximum_height=100            
    ):
    squares_array: list[QPushButton] = []
    index = 0
    for i in range(1, 9):
        for j in range(1, 9):
            squares_array.append(QPushButton(""))
            squares_array[index].clicked.connect(lambda state, x=i, y=j: squareClicked(x, y))
            squares_array[index].setStyleSheet(
                f"""background-color : {
                DARK if (j + i) % 2 != 0 else LIGHT
                }""")
            squares_array[index].setMinimumWidth(minimum_width)
            squares_array[index].setMinimumHeight(minimum_height)
            squares_array[index].setMaximumWidth(maximum_width)
            squares_array[index].setMaximumHeight(maximum_height)
            index += 1
    return squares_array


class Dama(QMainWindow):
    def __init__(self):
        super(Dama, self).__init__()
        self.init_UserInterface()

    def init_UserInterface(self):
        # Window Init
        self.wid = QWidget(self)
        self.setCentralWidget(self.wid)
        self.grid_layout = QGridLayout()

        # Menu Bar Init
        menu = QMenuBar()
        self.setMenuBar(menu)
        menu.setNativeMenuBar(False)

        change_appereance = QAction("Change Visuals", self)
        change_appereance.setStatusTip("Sets the Checkerboard in a High Contrast Color Palette")
        change_appereance.triggered.connect(lambda: self.changeAppearance())

        zoom_in = QAction("Zoom '+' Overflow", self)
        zoom_in.setStatusTip("Resizes the Board by a factor. After a certain threshold, changes also the aspect ratio")
        zoom_in.triggered.connect(lambda: self.zoom_in())

        zoom_out = QAction("Zoom Reset", self)
        zoom_out.setStatusTip("Resets the board Zoom")
        zoom_out.triggered.connect(lambda: self.zoom_reset())

        file = QMenu("&File", self)             # File Menu
        menu.addMenu(file)

        visuals = QMenu("&Visuals", self)       # Visual Aid Menu
        visuals.addAction(change_appereance)    
        visuals.addAction(zoom_in)
        visuals.addAction(zoom_out)
        menu.addMenu(visuals)

        settings = QMenu("&Settings", self)     # Settings Menu
        menu.addMenu(settings)

        self.setGeometry(0, 0, 800, 800)
        self.setWindowTitle("etti®'s online dama")

        # Initial Board Placement
        buttons = refresh_board(DARK_BROWN, LIGHT_BROWN)
        self.update_board(buttons)

    def update_board(self, buttons: list[QPushButton]):
        index = 0
        for i in range(1, 9):
            for j in range(1, 9):
                self.grid_layout.addWidget(buttons[index], i, j)
                index += 1
        self.wid.setLayout(self.grid_layout)

    def changeAppearance(self):
        global CLR_MODE

        if CLR_MODE % 2 == 0:
            buttons = refresh_board(HC_BLACK, HC_YELLOW)
        else:
            buttons = refresh_board(DARK_BROWN, LIGHT_BROWN)

        CLR_MODE += 1

        self.update_board(buttons)

        self.wid.setLayout(self.grid_layout)

    def zoom_in(self):
        global H, W
        H += 300
        W += 300
        self.setGeometry(0, 0, H, W)
        buttons = refresh_board(minimum_height=130)
        self.update_board(buttons)

    def zoom_reset(self):
        global H, W
        H = 800
        W = 800
        buttons = refresh_board(
            minimum_height=100,
            minimum_width=100,
            maximum_height=100,
            maximum_width=100
            )
        self.update_board(buttons)
        self.resize(800, 800)



def main():
    app = QApplication(sys.argv)
    win = Dama()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
