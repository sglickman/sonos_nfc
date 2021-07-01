import soco

def replace_queue_with_album_list(album_list):
  coordinator = get_tv_room().group.coordinator
  #tv_room.unjoin()
  coordinator.clear_queue()
  for artist, album in album_list:
    tracklist = coordinator.music_library.get_tracks_for_album(artist.encode('utf-8'), album.encode('utf-8'))
    if len(tracklist) == 0:
      print("No tracks found for " + artist + " | " + album)
    else:
      print("Adding tracks for " + artist + " | " + album)
      coordinator.add_multiple_to_queue(tracklist)
      coordinator.play()

def get_tv_room():
  players = list(soco.discover())
  for player in players:
    if "TV" in player.player_name:
      return player
