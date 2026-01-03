from constants import *

class CountdownDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configurar tiempo")

        layout = QVBoxLayout(self)

        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm:ss")
        self.time_edit.setTime(QTime(0, 5, 0))
        layout.addWidget(self.time_edit)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_time_seconds(self):
        t = self.time_edit.time()
        return t.hour() * 3600 + t.minute() * 60 + t.second()


class TimeEditDialog(QDialog):
    def __init__(self, time: QTime, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Editar tiempo")
        self.setFixedSize(220, 100)

        layout = QVBoxLayout(self)

        self.time_edit = QTimeEdit(time)
        self.time_edit.setDisplayFormat("HH:mm:ss")
        self.time_edit.setAlignment(Qt.AlignCenter)
        self.time_edit.setFocus(Qt.OtherFocusReason)
        self.time_edit.selectAll()

        self.time_edit.setStyleSheet("""
            QTimeEdit {
                font-size: 24px;
            }
        """)

        layout.addWidget(self.time_edit)

        # ENTER confirma automáticamente
        self.time_edit.editingFinished.connect(self.accept)

    def get_time(self):
        return self.time_edit.time()


# ======================================================
# TIMER (simplificado, funcional)
# ======================================================

class TimerWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.mode = "Chronometer"
        self.state = "Stop"

        self.base_time = QTime(0, 0, 0)
        self.progress_time = QTime(0, 0, 0)

        # ---------- MODE BUTTON ----------
        self.mode_btn = QPushButton("⏱ Cronómetro")
        self.mode_btn.clicked.connect(self.toggle_mode)
        self.mode_btn.setStyleSheet("""
            QPushButton {
                background: none;
                border: none;
                color: #cccccc;
                font-size: 14px;
                text-align: left;
            }
            QPushButton:hover { color: white; }
        """)

        # ---------- CLOCK ----------
        self.clock = QTimeEdit()
        self.clock.setDisplayFormat("HH:mm:ss")
        self.clock.setAlignment(Qt.AlignCenter)
        self.clock.setReadOnly(True)
        self.clock.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.clock.setFocusPolicy(Qt.NoFocus)
        self.clock.setTime(self.progress_time)

        self.clock.setStyleSheet("""
            QTimeEdit {
                font-size: 36px;
                font-weight: bold;
                color: white;
                background: transparent;
                border: none;
            }
        """)

        self.clock.installEventFilter(self)
        self.click = ClickWidget()


        # ---------- BUTTONS ----------
        style = self.style()

        self.play_btn = QToolButton()
        self.play_btn.setIcon(style.standardIcon(QStyle.SP_MediaPlay))
        self.play_btn.setIconSize(QSize(32, 32))

        self.reset_btn = QToolButton()
        self.reset_btn.setIcon(style.standardIcon(QStyle.SP_MediaStop))
        self.reset_btn.setIconSize(QSize(32, 32))

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.addWidget(self.play_btn)
        btn_layout.addWidget(self.reset_btn)

        # ---------- LAYOUT ----------
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.addWidget(self.mode_btn)
        layout.addWidget(self.clock)
        layout.addLayout(btn_layout)

        # ---------- TIMER ----------
        self._qtimer = QTimer(self)
        self._qtimer.timeout.connect(self.advance_time)
        self._qtimer.start(1000)

        # ---------- CONNECTIONS ----------
        self.play_btn.clicked.connect(self.toggle)
        self.reset_btn.clicked.connect(self.reset)

    # ==================================================
    # MODE
    # ==================================================

    def toggle_mode(self):
        self.state = "Stop"
        self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        if self.mode == "Chronometer":
            self.mode = "Countdown"
            self.mode_btn.setText("⏳ Temporizador")
            self.base_time = QTime(0, 5, 0)             # Caso básico de cuenta regresiva
            self.progress_time = self.base_time
        else:
            self.mode = "Chronometer"
            self.mode_btn.setText("⏱ Cronómetro")
            self.base_time = QTime(0, 0, 0)
            self.progress_time = QTime(0, 0, 0)

        self.clock.setTime(self.progress_time)

    # ==================================================
    # EDIT MODE
    # ==================================================
    def eventFilter(self, obj, event):
        if obj is self.clock and event.type() == QEvent.Type.MouseButtonPress and self.mode == "Countdown":
            self.open_time_editor()
            return True
        
        return super().eventFilter(obj, event)




    

    def open_time_editor(self):
        print('Open time editor')
        # Frenar el timer
        self.state = "Stop"
        self.play_btn.setIcon(
            self.style().standardIcon(QStyle.SP_MediaPlay)
        )

        dialog = TimeEditDialog(self.base_time, self)

        if dialog.exec():
            self.base_time = dialog.get_time()
            self.progress_time = self.base_time
            self.clock.setTime(self.progress_time)




    # ==================================================
    # TIMER LOGIC
    # ==================================================

    def advance_time(self):
        if self.state != "Run":
            return


        if self.mode == "Chronometer":
            self.progress_time = self.progress_time.addSecs(1)
        else:
            if self.progress_time > QTime(0, 0, 0):
                self.progress_time = self.progress_time.addSecs(-1)
            else:
                self.state = "Stop"
                self.play_btn.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay)
                )

        self.clock.setTime(self.progress_time)

    def toggle(self):
        if self.state == "Run":
            self.state = "Stop"
            self.play_btn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
            )
        else:
            self.state = "Run"
            self.play_btn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
            )

    def reset(self):
        self.state = "Stop"
        self.play_btn.setIcon(
            self.style().standardIcon(QStyle.SP_MediaPlay)
        )

        self.progress_time = self.base_time
        self.clock.setTime(self.progress_time)

