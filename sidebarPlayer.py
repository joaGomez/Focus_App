from constants import *

import pygame
import time
from mutagen.mp3 import MP3
import msvcrt





class AudioPlayer():
    def __init__(self):
        super().__init__()
        
        try:
            pygame.mixer.init()
            
        except pygame.error as e:
            print("Audio init failed!", e)

        self.audio_path = None
        self.audio = None
        self.total_duration = 0
        self.current_time = 0.0
        self.state = PlayerState.STOPPED
        self.volume = 0.5
        
        
        
        
    def set_audio_player(self, audio_file_path):
        self.audio = MP3(audio_file_path)
        self.total_duration = self.audio.info.length
        pygame.mixer.music.load(audio_file_path)
        pygame.mixer.music.set_volume(self.volume)      
        
        
    def set_audio_player_volume(self, volume):
        self.volume = volume


    def set_audio_player_state(self, newState):
       
        self.state = newState       # New state for audio player

        if self.state == PlayerState.PLAYING:
            pygame.mixer.music.play()

        elif self.state == PlayerState.PAUSED:
            pygame.mixer.music.pause()

        elif self.state == PlayerState.STOPPED:
            pygame.mixer.music.stop()
    
        


class SidebarPlayer(QWidget):
    def __init__(self, refresh_callback_play_button = None):
        super().__init__()

        self.current_playlist = None
        self.current_index = 0
        
        self.refresh_callback = refresh_callback_play_button

        # ---- MEDIA PLAYER ----
        self.audioPlayer = AudioPlayer()

        # ---- BOTONES ----
        self.btn_prev = QPushButton("⏮")
        self.btn_play = QPushButton("▶")
        self.btn_next = QPushButton("⏭")

        self.btn_prev.setFixedSize(40, 40)
        self.btn_play.setFixedSize(50, 50)
        self.btn_next.setFixedSize(40, 40)

        # ---- TIEMPO ----
        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setAlignment(Qt.AlignCenter)

        # ---- SLIDER ----
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 1000)

        # ---- LAYOUT ----
        controls = QHBoxLayout()
        controls.addWidget(self.btn_prev)
        controls.addWidget(self.btn_play)
        controls.addWidget(self.btn_next)

        layout = QVBoxLayout(self)
        layout.addWidget(self.time_label)
        layout.addWidget(self.slider)
        layout.addLayout(controls)

        # ---- SIGNALS ----
        self.btn_play.clicked.connect(self.toggle_play)
        self.btn_prev.clicked.connect(self.previous_track)
        self.btn_next.clicked.connect(self.next_track)

        self.slider.sliderMoved.connect(self.seek)

        # self.player.positionChanged.connect(self.update_position)
        # self.player.durationChanged.connect(self.update_duration)
        # self.player.mediaStatusChanged.connect(self.check_finished)

        # ---- STYLE ----
        self.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border-radius: 10px;
            }
            QLabel { color: white; }
        """)

   
    # ======================================================
    # API llamada por MainWindow
    # ======================================================
    def set_playlist(self, playlist: dict):
        
        if self.current_playlist == playlist:       # no index reset when same playlist selected
            return
        
        self.current_playlist = playlist
        self.current_index = 0
        # self.load_track(0)
        
        print(f'Playlist seleccionada: {playlist}')
        
        if playlist:
            print(f'Audio seleccionado: {self.current_playlist["tracks"][self.current_index]}')
        

    # ======================================================
    # CONTROLES
    # ======================================================
    def toggle_play(self):
        if self.audioPlayer.state == PlayerState.PLAYING:
            self.audioPlayer.set_audio_player_state(PlayerState.PAUSED)     # Pause audio output
            # self.btn_play.setText("▶")
        elif self.audioPlayer.state == PlayerState.PAUSED or self.audioPlayer.state == PlayerState.STOPPED:
            self.audioPlayer.set_audio_player_state(PlayerState.PLAYING)    # Continues audio output
            # self.btn_play.setText("⏸")
            
        if self.refresh_callback:
            self.refresh_callback(self.audioPlayer.state)
    
    def plot_play_button(self, state):
        if state == PlayerState.PAUSED or state == PlayerState.STOPPED:
            self.btn_play.setText("▶")
        elif state == PlayerState.PLAYING:
            self.btn_play.setText("⏸")
        

    def previous_track(self):
        if not self.current_playlist: return
        
        if self.audioPlayer.current_time >= 1.0:
            self.audioPlayer.current_time = 0.0                         # Same song but it restarts

        else:
            self.current_index = max(0, self.current_index - 1)         # Index cant be less than 0 (First song)
            self.audioPlayer.current_time = 0.0                         # New song must start form 0:00
            
        
        # Set audio file to audio player
        
        audio_path = self.current_playlist["tracks"][self.current_index]
        
        self.audioPlayer.set_audio_player(audio_file_path = audio_path)
            

    def next_track(self):

        if self.current_index < (len(self.current_playlist["tracks"])-1):
            
            self.current_index = self.current_index + 1                             # Next song
            self.audioPlayer.current_time = 0.0                                     # New song must start form 0:00
            
        elif self.current_index == (len(self.current_playlist["tracks"])-1):
            self.current_index = 0                                                  # Restarts playlist
            self.audioPlayer.current_time = 0.0                                     # New song must start form 0:00

            # Auto restart ?
            # if not auto_restart:                                                          # if auto restart selected -> Playlist restarts and continues playing. ELse, not.
            #     self.audioPlayer.set_audio_player_state(PlayerState.STOPPED)
            
            
            
        # Set audio file to audio player
        
        audio_path = self.current_playlist["tracks"][self.current_index]
        
        self.audioPlayer.set_audio_player(audio_file_path = audio_path)

    # ======================================================
    # CARGA
    # ======================================================
    # def load_track(self, index):
    #     if not self.current_playlist:
    #         return
        
    #     # self.audioPlayer.set_audio_player()
        
    #     audio = self.current_playlist["tracks"][index]
    #     url = QUrl.fromLocalFile(audio)


    #     print('Audio seleccionado')
    #     print(audio)
    #     print('URL del audio seleccionado')
    #     print(url)


    #     self.player.setSource(url)
    #     self.player.play()
    #     self.btn_play.setText("⏸")

    # ======================================================
    # TIEMPO Y SLIDER
    # ======================================================
    def update_position(self, pos):
        if self.player.duration() > 0:
            percent = int(pos / self.player.duration() * 1000)
            self.slider.setValue(percent)

        self.update_time_label()

    def update_duration(self, dur):
        self.update_time_label()

    def update_time_label(self):
        pos = self.player.position() // 1000
        dur = self.player.duration() // 1000

        def fmt(x):
            m, s = divmod(x, 60)
            return f"{m:02}:{s:02}"

        self.time_label.setText(f"{fmt(pos)} / {fmt(dur)}")

    def seek(self, value):
        if self.player.duration() > 0:
            new_pos = int(self.player.duration() * (value / 1000))
            self.player.setPosition(new_pos)

    # ======================================================
    # FINAL AUTOMÁTICO
    # ======================================================
    def check_finished(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.next_track()