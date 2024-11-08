## importing libraries
import spotipy
import requests
import uuid
import time
from spotipy.oauth2 import SpotifyClientCredentials

client_id = "SPOTIFY_CLIENT_ID"
client_secret = "SPOTIFY_CLIENT_SECRET"



## found in app, adresses for each light module
address1 = "LIGHT_ADDRESS_1"
address2 = "LIGHT_ADDRESS_2"
address3 = "LIGHT_ADDRESS_3"

## specific track URI to analyse
track_uri = "TRACK_URI"





## API information for company's API
api_key = "API_KEY"
cmdEndpt = 'COMMAND_ENDPOINT'

cmdHead={"X-API-Key":api_key,
  "accessKey":"ACCESS_KEY",
  "secretKey":"SECRET_KEY",
  "Content-Type": "application/json"}

def get_uuid():
    return str(uuid.uuid4())

## pads values down to a specific size
def padding(x, sze):
    if (len(x) < sze):
        for i in range (0, (sze - len(x))):
            x = "0" + x
    x = x.upper()
    return x

## converts rgbw to hex
def converter(r, g, b, w):
    r = format(r, 'x')
    r = padding(r, 4)
    g = format(g, 'x')
    g = padding(g, 4)
    b = format(b, 'x')
    b = padding(b, 4)
    w = format(w, 'x')
    w = padding(w, 4)
    return r, g, b, w

## function that posts the same color to all the light modules
def postall_to_bridge(postColor):
  r, g, b, w = converter(postColor.red, postColor.green, postColor.blue, postColor.white)
  param = r + g + b + w 
  Type = 0 #0 = all sendout
  cmd = {
    "param": param,
    "cloudUUID": get_uuid(),
    "createdTimestamp": int((1000 * time.time())),
    "type": Type,
    "syncTimestamp": int((1000 * time.time())),
    }
  r = requests.post(cmdEndpt, headers=cmdHead, json=cmd)

## function that posts single color to a single module
def postsingle_to_bridge(postColor, address):
  r, g, b, w = converter(postColor.red, postColor.green, postColor.blue, postColor.white)
  param = r + g + b + w + address
  Type = 1 #1 = single sendout
  cmd = {
    "param": param,
    "cloudUUID": get_uuid(),
    "createdTimestamp": int((1000 * time.time())),
    "type": Type,
    "syncTimestamp": int((1000 * time.time())),
    }
  r = requests.post(cmdEndpt, headers=cmdHead, json=cmd)


class color:
  def __init__(self, red, green, blue, white):
    self.red = red
    self.green = green
    self.blue = blue
    self.white = white

 

## Create an instance (object) for each color, setting the rgbw values

red = color(1023, 0, 0, 0 )
orange = color(381, 131, 0, 0)
yellow = color(302, 305, 0, 0)
green = color(0, 1023, 0, 0)
blue = color(0, 0, 1023, 0)
purple = color(121, 0, 1023, 0)
white = color(0, 0, 0, 1023)


## function gets audio data from track, extracts the energy, valanve, and mode of the song
def get_spotify_data(track_uri):
  
  client = spotipy.Spotify(
      auth_manager=SpotifyClientCredentials(client_id, client_secret)
  )

  audio_features = client.audio_features([track_uri])
    # fail safe
  if not audio_features:
      return {"error": "Failed to retrieve audio features"}
    # extracts energy val, stores in var
  energy = audio_features[0]["energy"]
  valence = audio_features[0]["valence"]
  mode = audio_features[0]["mode"]
  
    # calls color function after vals are stored
  color_calculation(valence, mode, energy)


def color_calculation(valence, mode, energy):
  # logic for color matching,, ranges

    if valence >=0 and valence <=0.340:
        color1 = purple
    elif valence >=0.341 and valence <=0.667:
        color1 = orange
    elif valence >=0.668 and valence <=1:
        color1 = yellow

    if mode == 0:
        color2 = blue
    elif mode == 1:
        color2 = yellow
    
    if energy >=0 and energy <=0.340:
        color3 = blue
    elif energy >=0.341 and energy <=0.667:
        color3 = orange
    elif energy >=0.668 and energy <=1:
        color3 = red
    
    # prints values
  
    print(f"valence = {valence}")
    print(f"mode = {mode}")
    print(f"energy = {energy}")

    ## bridge has a delay of 5ish seconds btwn commands
    postsingle_to_bridge(color1, address1)
    postsingle_to_bridge(color2, address2)
    postsingle_to_bridge(color3, address3)


## calls the one function :)
get_spotify_data(track_uri)

