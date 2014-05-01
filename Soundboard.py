# Soundboard
# Copyright 2014 Tony DiCola
# Released under an MIT license. (http://opensource.org/licenses/MIT)

# Simple flask application to create a soundboard that is accessible over the web.
# Requires the flask web framework and madplay is installed.
# Copy MP3 files into the sounds subdirectory, then run the this script with python.
# Access http://<machine IP address>:5000/ in a browser to access the soundboard.

import fnmatch
import os
import os.path
from subprocess import Popen

from flask import *


# Configuration
MADPLAY_ATTENUATE = -12		# This controls the attenuation of the audio, in decibels.
							# Negative values will reduce the volume, positive will increase it.

SOUND_DIR = './sounds/'		# Directory which contains sound files (as MP3s).

PORT = 5000					# Port to use for the server.


# Change to the directory where the script lives so relative dirs resolve correctly.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Global reference to the audio playback process.
madplay = None

# Create flask application.
app = Flask(__name__)


# Play the specified MP3 file.
def play_sound(filename):
	global madplay
	# Stop audio if it's playing.
	stop_sound()
	# Invoke madplay to play audio.
	madplay = Popen(['madplay',
					 '--attenuate={0}'.format(MADPLAY_ATTENUATE),
					 './sounds/{0}'.format(filename)])

# Stop playing any audio.
def stop_sound():
	global madplay
	if madplay is not None:
		madplay.terminate()

# Return a list of all playable MP3 files.  Each list element is an object with a name 
# (filename minus extension) and file name property.
def list_sounds():
	return map(lambda f: { 'name': os.path.splitext(f)[0], 'filename': f }, 
			   fnmatch.filter(os.listdir(SOUND_DIR), '*.[Mm][Pp]3'))


# Define routes for web application.

# Root route displays the main page.
@app.route('/')
def root():
	return render_template('index.html', sounds=list_sounds())

# Play route will play the specified MP3.
@app.route('/play/<filename>', methods=['PUT'])
def play(filename):
	play_sound(filename)
	return ('OK', 200)

# Stop route will stop all audio playback.
@app.route('/stop', methods=['PUT'])
def stop():
	stop_sound()
	return ('OK', 200)


if __name__ == '__main__':
	# Create a server listening for external connections on the default
	# port 5000.  Enable debug mode for better error messages and live
	# reloading of the server on changes.  Also make the server threaded
	# so multiple connections can be processed at once.
	app.run(host='0.0.0.0', port=PORT, debug=True, threaded=True)
