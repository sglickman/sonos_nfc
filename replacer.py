import urllib2
import soco

def prep_for_sonos(uri):
  return uri.replace("?", "%3F") + ".mp3"

def replace_queue_with_album(album_id, sonos_player):
  print "replacing queue with album " + album_id
  m3u = urllib2.urlopen('http://raspberrypi:9999/get_album?id=' + album_id)
  lines = m3u.read().splitlines()
  print "m3u:"
  print lines
  sonos_player.unjoin()
  sonos_player.clear_queue()
  items = []
  for line in lines:
    if line.startswith('http'):
      items += [make_item_from_uri(prep_for_sonos(line))]
  sonos_player.add_multiple_to_queue(items)
  sonos_player.play()

#     # sonos_player.add_uri_to_queue(prep_for_sonos(line))
#     # sonos_player.play()

def replace_queue_with_song_list(song_list, sonos_player):
  print "replacing queue with song list (locker album) " + str(len(song_list))
  print song_list
  sonos_player.unjoin()
  sonos_player.clear_queue()
  items = [make_item_from_uri(prep_for_sonos('http://192.168.86.249:9999/get_song?id=' + uri)) for uri in song_list]
  print items
  sonos_player.add_multiple_to_queue(items)
  sonos_player.play()

def get_tv():
  players = list(soco.discover())
  for player in players:
    if "TV" in player.player_name:
      return player

def make_item_from_uri(uri):
  res = [soco.data_structures.DidlResource(uri=uri, protocol_info="x-rincon-playlist:*:*:*")]
  item = soco.data_structures.DidlObject(resources=res, title='', parent_id='', item_id='')
  return item
