from constants import *

from sidebar import Sidebar
from playlist import PlaylistCard, PlaylistsGrid, PlaylistView
from playlistManager import PlaylistManager



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.manager = PlaylistManager()        # Load every playlist from JSON playlists configuration

        self.setWindowTitle("Music Player")
        self.resize(1200, 700)

        central = QWidget()
        self.setCentralWidget(central)
        central_layout = QVBoxLayout(central)

        self.playlist_view = PlaylistView(refresh_callback_playlist = self.update_playlist_selected, 
                                          refresh_callback_state = self.update_playlist_state, 
                                          refresh_callback_play_button = self.update_play_button)     # Playlist Selected

        self.playlists_grid = PlaylistsGrid(
            self.playlist_view,
            self.manager.get_playlists()     
        )                                       # Playlists list in grid format. You can scroll to see every playlist

        central_layout.addWidget(self.playlist_view)
        central_layout.addWidget(self.playlists_grid)

        # Sidebar
        dock = QDockWidget("Configuración", self)
        # sidebar = Sidebar(self.manager)      
        
        
        self.manager = PlaylistManager()        # Manages every change that happens on playlists

        self.sidebar = Sidebar(
            self.manager,
            self.playlist_view,
            refresh_callback = self.refresh_playlists,
            refresh_callback_play_button_player=self.update_play_button,
            refresh_callback_state = self.update_playlist_state
        )
        
        dock.setWidget(self.sidebar)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
    
    
    def refresh_playlists(self):                        # Update changes form playlists
        playlists = self.manager.get_playlists()
        self.playlists_grid.update_grid(playlists)
        
    def update_playlist_selected(self):
        playlist_title = self.playlist_view.playlist_title
        playlist_selected = self.manager.get_playlist(playlist_title)
        
        self.sidebar.player.set_playlist(playlist_selected)
        
        # Set audio file to audio player
        audio_path = self.sidebar.player.current_playlist["tracks"][self.sidebar.player.current_index]
        
        self.sidebar.player.audioPlayer.set_audio_player(audio_file_path = audio_path)
        
        self.sidebar.player.restart_timer()    
        
    
        
        
        
        
        
        
        
    def update_playlist_state(self, newState):
        if self.sidebar.player.current_playlist:                        # Playlist not null
            self.sidebar.player.audioPlayer.set_audio_player_state(newState)
            
            if newState == PlayerState.PLAYING:
                self.sidebar.player.timer.start()
                
            elif newState in (PlayerState.STOPPED, PlayerState.PAUSED):
                self.sidebar.player.timer.stop()
            
            
        
            
    def update_play_button(self, newState):
        if self.sidebar.player.current_playlist:                        # Playlist not null
            self.sidebar.player.plot_play_button(newState)              # Update play button on sidebar
            self.playlist_view.plot_play_button(newState)               # Update play button in playlist view
            