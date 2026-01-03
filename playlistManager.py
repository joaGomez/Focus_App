import json
import os

class PlaylistManager:
    def __init__(self, path="Data/playlists.json"):
        self.path = path
        self.playlists = []
        self.load()

    def load(self):
        """Carga playlists desde JSON."""
        if not os.path.exists(self.path):
            self.playlists = []
            return

        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.playlists = data.get("playlists", [])
            print('Playlists cargadas al programa')
            print(self.playlists)

    def save(self):
        """Guarda playlists en JSON."""
        data = {"playlists": self.playlists}
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def add_playlist(self, name, cover, tracks):
        """Agrega una playlist nueva."""
        playlist = {
            "name": name,
            "cover": cover,
            "tracks": tracks
        }
        self.playlists.append(playlist)
        self.save()

    # def remove_playlist(self, name):
    #     """Elimina playlist por nombre."""
    #     self.playlists = [
    #         p for p in self.playlists if p["name"] != name
    #     ]
    #     self.save()

    def get_playlists(self):
        return self.playlists

    def get_playlist(self, name):
        """Devuelve una playlist por nombre."""
        for p in self.playlists:
            if p["name"] == name:
                return p
        return None
