from constants import *


# ======================================================
# PLAYLIST CARD (título superpuesto)
# ======================================================

class PlaylistCard(QWidget):
    def __init__(self, title, image_path, callback):
        super().__init__()

        self.title = title
        self.image_path = image_path
        self.callback = callback

        self.setFixedSize(160, 200)

        # --- CONTENEDOR PRINCIPAL ---
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Contenedor con imagen y título superpuesto
        container = QWidget()
        container.setFixedSize(160, 200)

        stack = QStackedLayout(container)

        # Imagen
        self.image = QLabel()
        pixmap = QPixmap(image_path).scaled(
            160, 200, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )
        self.image.setPixmap(pixmap)
        self.image.setAlignment(Qt.AlignCenter)

        # Título superpuesto arriba
        self.label = QLabel(title)
        self.label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.label.setStyleSheet("""
            color: white;
            font-weight: bold;
            font-size: 16px;
            padding-top: 6px;
            background-color: rgba(0, 0, 0, 60);
        """)

        # Apilamos la imagen y el título uno encima del otro
        stack.addWidget(self.image)
        stack.addWidget(self.label)

        layout.addWidget(container)

        # Estilo del card
        self.setStyleSheet("""
            QWidget {
                border-radius: 10px;
                background-color: #1f1f1f;
            }
            QWidget:hover {
                background-color: #2b2b2b;
            }
        """)

    def mousePressEvent(self, event):
        self.callback(self.title, self.image_path)
        # print(f'Se selecciono la playlist: {self.title}')


# ======================================================
# PLAYLIST VIEW (vista grande con botón Play/Pause)
# ======================================================

class PlaylistView(QWidget):
    def __init__(self, refresh_callback_playlist=None, 
                 refresh_callback_state=None, 
                 refresh_callback_play_button=None):
        super().__init__()

        self.current_image_path = None
        self.playlist_title = None
        self.state = PlayerState.STOPPED        # Inner state to for easier logic control   
        
        self.refresh_callback_playlist = refresh_callback_playlist
        self.refresh_callback_state = refresh_callback_state
        self.refresh_callback_play_button = refresh_callback_play_button

        self.main_layout = QVBoxLayout(self)

        # === IMAGEN ===
        self.image = QLabel("Seleccioná una playlist")
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setStyleSheet("color: gray;")
        self.image.setMinimumHeight(250)
        self.image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.main_layout.addWidget(self.image)

        # === TITULO + BOTÓN ===
        self.info_layout = QVBoxLayout()

        # Título (oculto al inicio)
        self.title = QLabel("")
        self.title.setAlignment(Qt.AlignLeft)
        self.title.setStyleSheet("""
            font-size: 26px; 
            color: white; 
            font-weight: bold;
        """)
        self.title.hide()              # <---- Ocultamos inicialmente 
        self.info_layout.addWidget(self.title)

        # Botón reproducir/pausar (oculto al inicio)
        self.play_button = QPushButton("Reproducir")
        self.play_button.setFixedSize(160, 42)
        self.play_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e6e6e6;
            }
        """)
        self.play_button.hide()        # <---- Ocultamos inicialmente
        self.info_layout.addWidget(self.play_button, alignment=Qt.AlignLeft)

        self.info_layout.addStretch()
        self.main_layout.addLayout(self.info_layout)

        
        
        
        
        self.play_button.clicked.connect(self.toggle_play)


    # ====================================================
    # Cuando seleccionás una playlist
    # ====================================================
    def set_playlist(self, title, image_path):
        self.current_image_path = image_path
        self.playlist_title = title
        
        print(self.playlist_title)

        # Mostrar título y botón
        self.title.setText(title)
        self.title.show()
        self.play_button.show()

        self.state = PlayerState.STOPPED
        
        self.play_button.setText("Reproducir")
        self.update_image()
        
        if self.refresh_callback_playlist:
            self.refresh_callback_playlist()
            
        if self.refresh_callback_state:
            self.refresh_callback_state(self.state)



    # ====================================================
    # Ajusta imagen cuando se redimensiona
    # ====================================================
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_image()


    def update_image(self):
        if not self.current_image_path:
            
            # Estado sin playlist seleccionada
            
            self.image.setText("Seleccioná una playlist")
            self.image.setPixmap(QPixmap())                     # Limpia imagen previa
            return

        pixmap = QPixmap(self.current_image_path)

        scaled = pixmap.scaled(
            self.image.width(),
            self.image.height(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        self.image.setPixmap(scaled)


    # ====================================================
    # Botón reproducir/pausar
    # ====================================================
    def toggle_play(self):
        
        if self.state == PlayerState.STOPPED or self.state == PlayerState.PAUSED:
            self.state = PlayerState.PLAYING
            
            
        elif self.state == PlayerState.PLAYING:
            self.state = PlayerState.PAUSED
            
        if self.refresh_callback_state:
            self.refresh_callback_state(self.state)
        
        if self.refresh_callback_play_button:
            self.refresh_callback_play_button(self.state)
                        
        
                
        
    def plot_play_button(self, state):
        if state == PlayerState.PAUSED or state == PlayerState.STOPPED:
            self.play_button.setText("Reproducir")
        elif state == PlayerState.PLAYING:
            self.play_button.setText("Pausar")
        
    



# ======================================================
# GRID DE PLAYLISTS
# ======================================================

class PlaylistsGrid(QScrollArea):
    def __init__(self, playlist_view, playlists):
        super().__init__()

        self.container = QWidget()
        self.layout = QGridLayout(self.container)
        self.playlist_view = playlist_view

        self.draw_grid(playlists)               # Draws grid for every playlist in the folder
    
    def draw_grid(self, playlists):
        for i, playlist in enumerate(playlists):
            card = PlaylistCard(
                playlist["name"],
                playlist["cover"],
                self.playlist_view.set_playlist
            )
            self.layout.addWidget(card, 0, i)

        self.setWidget(self.container)
        self.setWidgetResizable(True)
        self.setFixedHeight(230)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
    def update_grid(self, playlists):
        # 1) Borrar widgets anteriores
        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    widget.setParent(None)
                    widget.deleteLater()

        # 2) Agregar widgets nuevos
        self.draw_grid(playlists)
        