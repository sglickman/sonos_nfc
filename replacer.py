import soco

def replace_queue_with_album_list(album_list):
  tv_room = get_tv_room()
  tv_room.unjoin()
  tv_room.clear_queue()
  for artist, album in album_list:
    tracklist = tv_room.music_library.get_tracks_for_album(str(artist), str(album))
    if len(tracklist) == 0:
      print("No tracks found for " + artist + " | " + album)
    else:
      print("Adding tracks for " + artist + " | " + album)
      tv_room.add_multiple_to_queue(tracklist)
      tv_room.play()

def get_tv_room():
  players = list(soco.discover())
  for player in players:
    if "TV" in player.player_name:
      return player