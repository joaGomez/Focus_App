import sys, os

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTimeEdit,
    QGridLayout, QScrollArea, QDockWidget, QDialog, QAbstractSpinBox,
    QComboBox, QToolButton, QDialogButtonBox, QDateTimeEdit, QStackedLayout, QSizePolicy,
    QStyle, QLabel, QSlider, QFileDialog, QListWidgetItem, QListWidget, QLineEdit
)

from PySide6.QtGui import QPixmap, QMouseEvent

from PySide6.QtCore import (
    Qt, QTimer, QTime, Slot, QSize, QEvent, Signal, 
    QPropertyAnimation, QEasingCurve, QUrl
)

from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

from enum import Enum


# Estados posibles del reproductor de audio
class PlayerState(Enum):
    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"
    BUFFERING = "buffering"
    SEEKING = "seeking"
    ENDED = "ended"
    ERROR = "error"





class ClickWidget(QWidget):
    pressPos = None
    clicked = Signal()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressPos = event.pos()

    def mouseReleaseEvent(self, event):
        # ensure that the left button was pressed *and* released within the
        # geometry of the widget; if so, emit the signal;
        if (self.pressPos is not None and 
            event.button() == Qt.LeftButton):
                self.clicked.emit()
                print('Left click pressed')
        self.pressPos = None

