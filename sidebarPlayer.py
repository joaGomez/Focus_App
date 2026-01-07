from constants import *

import pygame
import time
from mutagen.mp3 import MP3
import msvcrt
from PySide6.QtCore import QTimer





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
        # pygame.mixer.music.play()
        
        if self.state == PlayerState.PLAYING:
            pygame.mixer.music.play()
        
        print('Se cargo el audio de la canción')
        
        
        
        
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
            
    def set_song_time(self, time):
        self.current_time = time
        pygame.mixer.music.set_pos(self.current_time)
    
        


class SidebarPlayer(QWidget):
    def __init__(self, refresh_callback_play_button = None,
                refresh_callback_state = None):
        super().__init__()

        self.current_playlist = None
        self.current_index = 0
        
        self.refresh_callback = refresh_callback_play_button
        self.refresh_callback_state = refresh_callback_state

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

        # ---- TIMER DE TIEMPO ----
        self.timer = QTimer()
        self.timer.setInterval(100)   # 100 ms
        self.timer.timeout.connect(self.update_time)
        self.timer_running = False



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
        
        # Reset states and buttons
        self.current_index = 0
        
        # new_song_duration = self.current_playlist["tracks"][self.current_index]
        
        self.update_time_label()
        
        self.plot_play_button(PlayerState.STOPPED)
        
        
        
        print(f'Playlist seleccionada: {playlist}')
        
        if playlist:
            print(f'Audio seleccionado: {self.current_playlist["tracks"][self.current_index]}')
        

    # ======================================================
    # CONTROLES
    # ======================================================
    def toggle_play(self):
        if self.audioPlayer.state == PlayerState.PLAYING:
            self.audioPlayer.set_audio_player_state(PlayerState.PAUSED)

        elif self.audioPlayer.state in (PlayerState.PAUSED, PlayerState.STOPPED):
            self.audioPlayer.set_audio_player_state(PlayerState.PLAYING)

        if self.refresh_callback:               # Updates play button
            self.refresh_callback(self.audioPlayer.state)
        
        if self.refresh_callback_state:         # Updates timer state
            self.refresh_callback_state(self.audioPlayer.state)

    
    def plot_play_button(self, state):
        if state == PlayerState.PAUSED or state == PlayerState.STOPPED:
            self.btn_play.setText("▶")
        elif state == PlayerState.PLAYING:
            self.btn_play.setText("⏸")
        

    
    def previous_track(self):
        if not self.current_playlist: return
        
        # If song started (timer >= 1.0s) -> Song restarts

        # If song first in the playlist, it must restart to itself -> No index change
        
        if self.audioPlayer.current_time < 1.0 and self.current_index != 0:     
            self.current_index = self.current_index - 1                  # Index from previous song
                
        self.restart_timer()                                                
        
        # Set audio file to audio player
        
        audio_path = self.current_playlist["tracks"][self.current_index]
        
        self.audioPlayer.set_audio_player(audio_file_path = audio_path)
                    
        print(f'Nueva canción en la fila: {self.audioPlayer.audio_path}')
    
        
        
            

    def next_track(self):
        
        if self.current_index < (len(self.current_playlist["tracks"])-1):
            self.current_index = self.current_index + 1                             # Next song
            
        elif self.current_index == (len(self.current_playlist["tracks"])-1):
            self.current_index = 0                              # Restarts playlist
            
            
            # Auto restart ?
            # if not auto_restart:                                                          # if auto restart selected -> Playlist restarts and continues playing. ELse, not.
            #     self.audioPlayer.set_audio_player_state(PlayerState.STOPPED)

        # Set audio file to audio player
        
        audio_path = self.current_playlist["tracks"][self.current_index]
        
        print(f'Nueva canción: {audio_path}')
        
        self.audioPlayer.set_audio_player(audio_file_path = audio_path)

        self.restart_timer()                                                    # New song must start form 0:00


    def update_time(self):
        if self.audioPlayer.state != PlayerState.PLAYING:
            return

        # avanzar el tiempo local
        self.audioPlayer.current_time += 0.1  # porque timer = 100ms

        # si se pasa del total → siguiente canción
        if self.audioPlayer.current_time >= self.audioPlayer.total_duration:
            self.next_track()
            return

        # Actualizar slider
        if self.audioPlayer.total_duration > 0:
            percent = int((self.audioPlayer.current_time / self.audioPlayer.total_duration) * 1000)
            self.slider.setValue(percent)

        # actualizar label
        self.update_time_label()
        
        
    def restart_timer(self):
        self.audioPlayer.current_time = 0.0                                     
        self.update_time_label()
        self.slider.setValue(0)



    # ======================================================
    # TIEMPO Y SLIDER
    # ======================================================
    def update_position(self, pos):
        if self.player.duration() > 0:
            percent = int(pos / self.player.duration() * 1000)
            self.slider.setValue(percent)

        self.update_time_label()




    def update_time_label(self):
        pos = int(self.audioPlayer.current_time)
        dur = int(self.audioPlayer.total_duration)
        
        def fmt(x):
            m, s = divmod(x, 60)
            return f"{m:02}:{s:02}"

        self.time_label.setText(f"{fmt(pos)} / {fmt(dur)}")





    def seek(self, value):
        
        if self.audioPlayer.total_duration > 0:
            new_pos = int((value/1000) * self.audioPlayer.total_duration)
            self.audioPlayer.set_song_time(new_pos)
        
        
        
        # if self.player.duration() > 0:
        #     new_pos = int(self.player.duration() * (value / 1000))
        #     self.player.setPosition(new_pos)

    # ======================================================
    # FINAL AUTOMÁTICO
    # ======================================================
    def check_finished(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.next_track()