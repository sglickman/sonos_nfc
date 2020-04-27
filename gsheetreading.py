import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name(
        '.gsheet_credentials.json', scope)

gc = gspread.authorize(credentials)

def matchGMusicId(album_id):
  try:
    spreadsheet = gc.open("Vinyl NFC List")
    wks = spreadsheet.sheet1
    values_list = wks.col_values(1)
    row_id = values_list.index(str(album_id))
    row_vals = wks.row_values(row_id + 1)
    print row_vals
    gmusic_id = row_vals[3]
    print "GMusic ID: " + gmusic_id
    if gmusic_id.startswith("LOCKER"):
      locker_sheet = spreadsheet.worksheet("Collection Locker")
      locker_ids = locker_sheet.col_values(1)
      first_row_id = locker_ids.index(str(gmusic_id))
      row_vals = locker_sheet.row_values(first_row_id + 1)
      song_ids = [row_vals[6]]
      num_tracks = int(row_vals[4].split("|")[1])
      print "Number of tracks: " + str(num_tracks)
      for i in range(num_tracks - 1):
        row_vals = locker_sheet.row_values(first_row_id + 1 + i)
        song_ids += [row_vals[6]]
      return song_ids
    else:
      return gmusic_id
  except gspread.exceptions.APIError:
    global gc
    gc = gspread.authorize(credentials)
    return matchGMusicId(album_id)
