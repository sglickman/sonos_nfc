import nfc
import gsheetreading
import replacer

class TagReader:
  clf = nfc.ContactlessFrontend('usb')
  previous_id = None

  def workWithTag(self, tag):
    if tag.ndef is None:
      return False
    album_id = None
    for record in tag.ndef.records:
      print record.type
      if record.type == 'text/gmusic-link':
        print "Sheets id:" 
        print record.data
        album_id = record.data
    if (album_id is not None) and (album_id != self.previous_id):
      self.previous_id = album_id
      print "attempting to match against gspread"
      try:
        gmusic_match = gsheetreading.matchGMusicId(record.data)
        if type(gmusic_match) == list:
          replacer.replace_queue_with_song_list(gmusic_match, replacer.get_tv())
        else:
          replacer.replace_queue_with_album(gmusic_match, replacer.get_tv())
      except ValueError:
        print "Couldn't find album ID for record data: " + str(record.data)
    else:
      print "album_id is None or same as previous"
    return True

  def readTag(self):
    assert self.clf.open('usb') is True
    print "Listening for tag"
    tag = self.clf.connect(rdwr={'on-connect': self.workWithTag})
    self.clf.close()
    print "Closing clf"

def readLoop():
  tag_reader = TagReader()
  while True:
    print "readTag()"
    tag_reader.readTag()
    print "done with readTag()"

