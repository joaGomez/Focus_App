from constants import *


from timer import TimerWidget
from sidebarPlayer import SidebarPlayer

from playlistManager import PlaylistManager


class Sidebar(QWidget):
    def __init__(self, manager: PlaylistManager, playlist_view, 
                refresh_callback=None, 
                refresh_callback_play_button_player=None,
                refresh_callback_state = None):
        """
        manager → PlaylistManager
        refresh_callback → función para que MainWindow refresque el grid
        """
        super().__init__()

        self.manager = manager
        self.refresh_callback = refresh_callback
        self.refresh_callback_player = refresh_callback_play_button_player
        self.refresh_callback_state = refresh_callback_state
        
        
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(20)

        self.timer = TimerWidget()
        
        # --- Reproductor ---
        self.player = SidebarPlayer(refresh_callback_play_button=self.refresh_callback_player,
                                    refresh_callback_state=self.refresh_callback_state)
        self.layout.addWidget(self.player)
        
        self.player.set_playlist(playlist_view.playlist_title)
        
        
        

        self.layout.addWidget(self.timer)
        self.layout.addStretch()

        # layout.addWidget(QPushButton("Nueva playlist"))
        # layout.addWidget(QPushButton("Configuración"))
        
        
        
        # layout = QVBoxLayout(self)
        # layout.setSpacing(15)

        # ---------- BOTÓN: NUEVA PLAYLIST ----------
        btn_new = QPushButton("Nueva playlist")
        btn_new.clicked.connect(self.open_new_playlist_dialog)
        self.layout.addWidget(btn_new)

        # En el futuro acá irá el reproductor de música
        # self.layout.addWidget(self.player_widget)

        self.layout.addStretch()

    # ======================================================
    # DIALOGO PARA CREAR PLAYLISTS
    # ======================================================

    def open_new_playlist_dialog(self):
        dialog = NewPlaylistDialog(self.manager, self)
        if dialog.exec():
            # Si se creó una playlist nueva → refrescar UI
            if self.refresh_callback:
                self.refresh_callback()
                


# ======================================================
# DIALOGO COMPLETO
# ======================================================

class NewPlaylistDialog(QDialog):
    def __init__(self, manager: PlaylistManager, parent=None):
        super().__init__(parent)
        self.manager = manager

        self.setWindowTitle("Crear nueva playlist")
        self.setMinimumWidth(400)

        self.layout = QVBoxLayout(self)

        # ---------- Nombre ----------
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Nombre de la playlist")
        self.layout.addWidget(self.name_edit)

        # ---------- Portada ----------
        cover_layout = QHBoxLayout()
        self.cover_label = QLabel("Sin portada")
        self.cover_label.setAlignment(Qt.AlignCenter)
        self.cover_label.setFixedSize(120, 120)
        self.cover_label.setStyleSheet("background: #444; color: white;")

        btn_cover = QPushButton("Elegir portada")
        btn_cover.clicked.connect(self.choose_cover)

        cover_layout.addWidget(self.cover_label)
        cover_layout.addWidget(btn_cover)

        self.layout.addLayout(cover_layout)

        self.cover_path = None

        # ---------- Archivos de audio ----------
        self.list = QListWidget()
        self.layout.addWidget(self.list)

        btn_audio = QPushButton("Agregar audios")
        btn_audio.clicked.connect(self.add_audio_files)
        self.layout.addWidget(btn_audio)

        self.track_paths = []

        # ---------- Botones ----------
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.create_playlist)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)

    # ======================================================
    # Acciones
    # ======================================================

    def choose_cover(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Elegir portada",
            "Imagenes/",
            "Imágenes (*.png *.jpg *.jpeg)"
        )
        if file:
            self.cover_path = file
            pixmap = QPixmap(file).scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.cover_label.setPixmap(pixmap)
        else:
            self.cover_label.setText("Sin portada")

    def add_audio_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Elegir audios",
            "Audios/",
            "Audio (*.mp3 *.wav)"
        )
        if files:
            self.track_paths.extend(files)
            for f in files:
                self.list.addItem(QListWidgetItem(f))

    def create_playlist(self):
        name = self.name_edit.text().strip()
        if not name:
            return

        cover = self.cover_path if self.cover_path else "Imagenes/default.jpg"
        tracks = self.track_paths

        self.manager.add_playlist(name, cover, tracks)
        self.accept()


