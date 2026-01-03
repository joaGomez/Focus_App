from constants import *

from app import MainWindow


# ======================================================
#                   MAIN CODE
# ======================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
