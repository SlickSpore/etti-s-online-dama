# includes

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QGridLayout, QMainWindow, QApplication, QWidget, QMenuBar, QMenu, QAction
import sys


# Color CONSTANTS
CLR_MODE = 0                # color theme
LIGHT_BROWN = "#ebd586"     # standard Light Color
DARK_BROWN = "#4d3b2d"      # standard Dark Color
HC_YELLOW = "#ffff00"       # High Contrast Light Color
HC_BLACK = "#000000"        # High Contrast Dark Color
PLAYERS_COLORS = [
    "",
    "#ebd586",
    "#250000",
    "#ff0000",
    "#00ff00"
]
DARK = DARK_BROWN
LIGHT = LIGHT_BROWN


W = 800
H = 800
FONT_SZ = 50
ZOOM_FACTOR = 0

# GLOBALS
BUTTONS: list[QPushButton] = []
PIECES_POSITIONS = bytearray(64)

# trigger function for each CheckerBoard Button
def squareClicked(x, y):
    pass
# shows the array of the checkerboard
def place_board(
        DARK=DARK_BROWN,
        LIGHT=LIGHT_BROWN,
        minimum_width=100,
        minimum_height=100,
        maximum_width=100,
        maximum_height=100            
    ):
    global BUTTONS, PIECES_POSITIONS

    index = 0
    for i in range(1, 9):
        for j in range(1, 9):
            BUTTONS.append(QPushButton(""))
            BUTTONS[index].clicked.connect(lambda state, x=i, y=j: squareClicked(x, y))
            BUTTONS[index].setStyleSheet(
                f"""background-color : {
                DARK if (j + i) % 2 != 0 else LIGHT
                }""")
            BUTTONS[index].setMinimumWidth(minimum_width)
            BUTTONS[index].setMinimumHeight(minimum_height)
            BUTTONS[index].setMaximumWidth(maximum_width)
            BUTTONS[index].setMaximumHeight(maximum_height)
            index += 1

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
        change_appereance.triggered.connect(lambda: self.set_HCBoard())

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
        place_board(DARK_BROWN, LIGHT_BROWN)
        self.init_Board()
        self.init_Pieces()
        self.wid.setLayout(self.grid_layout)
    
    def init_Pieces(self):
        global PIECES_POSITIONS
        
        # player one's piecies
        row = 1
        index = 0
        for i in range(0, 3):
            for j in range(0, 8):
                if j%2 == row%2:
                    PIECES_POSITIONS[index] = 2
                index += 1
            row += 1

        # player two's piecies
        index += 16
        for i in range(5, 8):
            for j in range(0, 8):
                if j%2 == row%2:
                    PIECES_POSITIONS[index] = 1
                index += 1
            row += 1
        
        self.refresh_Board()

    def init_Board(self):
        index = 0
        for i in range(0,8):
            for j in range(0,8):
                self.grid_layout.addWidget(BUTTONS[index],i,j)
                index += 1

    def refresh_Board(self):
        index = 0
        for i in range(0,8):
            for j in range(0,8):
                PIECES_POSITIONS[index]
                if PIECES_POSITIONS[index] != 0:
                    BUTTONS[index].setText("#")
                BUTTONS[index].setStyleSheet(
                    f"""
                    background-color : {
                        DARK if (i+j) % 2 != 0 else LIGHT
                    };
                    color : {
                        PLAYERS_COLORS[
                            PIECES_POSITIONS[index]+CLR_MODE if PIECES_POSITIONS[index] != 0 else 0
                            ]
                    };
                    font-size:{
                        FONT_SZ
                    }px
                    """
                )
                index+=1

    def set_HCBoard(self):
        global CLR_MODE, DARK, LIGHT


        if CLR_MODE == 0:
            CLR_MODE = 2
            DARK = HC_BLACK
            LIGHT = HC_YELLOW
        else:
            CLR_MODE = 0
            DARK = DARK_BROWN
            LIGHT = LIGHT_BROWN
        
        self.refresh_Board()
        
    def zoom_in(self):
        global H,W,ZOOM_FACTOR

        H,W = (H+155, W+155)
        ZOOM_FACTOR += 1
        for i in range(0,64):
            BUTTONS[i].setMinimumHeight(100+(15*ZOOM_FACTOR))
            BUTTONS[i].setMinimumWidth(100+(15*ZOOM_FACTOR))
        self.resize(H,W)

    def zoom_reset(self):
        global H,W,ZOOM_FACTOR
        H,W = (800, 800)
        for i in range(0,64):
            BUTTONS[i].setMinimumHeight(100)
            BUTTONS[i].setMinimumWidth(100)
            BUTTONS[i].setMaximumHeight(100)
            BUTTONS[i].setMaximumWidth(100)
        ZOOM_FACTOR = 0
        self.resize(H,W)


def main():
    app = QApplication(sys.argv)
    win = Dama()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
