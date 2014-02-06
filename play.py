#from Tkinter import * 
#import tkSnack 

#root=Tk()
#root.withdraw()#in case you don't want to see a Tk window in your app 
#tkSnack.initializeSnack(root) 
#s=tkSnack.Sound(load="/home/simone/Musica/test.mp3") 
#s.play()
#import pyglet

#pyglet.options['audio'] = ('openal', 'directsound', 'alsa', 'silent')

#music = pyglet.media.load('/home/simone/Musica/test.mp3')
#music.play()
#player = pyglet.media.Player()
#player.queue(music)
#print player.volume
#player.play()

#pyglet.app.run()
'''
Created on 2012. 2. 19.
This module is for playing mp3 (limited) and wav formatted audio file
@author: John
'''
import pygame
 
def playsound(soundfile):
    """Play sound through default mixer channel in blocking manner.
       This will load the whole sound into memory before playback
    """  
    pygame.mixer.init()
    # If you want more channels, change 8 to a desired number. 8 is the default number of channel
    pygame.mixer.set_num_channels(8)
    # This is the sound channel
    voice = pygame.mixer.Channel(5)
    sound = pygame.mixer.Sound(soundfile)
    voice.play(sound)
 
#    pygame.init()
#    pygame.mixer.init()
#    sound = pygame.mixer.Sound(soundfile)
#    clock = pygame.time.Clock()
#    sound.play()
#    while pygame.mixer.get_busy():
#        print "Playing..."
#        clock.tick(1000)
 
def playmusic(soundfile):
    """Stream music with mixer.music module in blocking manner.
       This will stream the sound from disk while playing.
    """
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    pygame.mixer.music.load(soundfile)
    pygame.mixer.music.play()

def busy():
    while pygame.mixer.music.get_busy() == True:
        continue
    return 

 
def stopmusic():
    """stop currently playing music"""
    pygame.mixer.music.stop()
 
def getmixerargs():
    pygame.mixer.init()
    freq, size, chan = pygame.mixer.get_init()
    return freq, size, chan
 
 
def initMixer():
	BUFFER = 3072  # audio buffer size, number of samples since pygame 1.8.
	FREQ, SIZE, CHAN = getmixerargs()
	pygame.mixer.init(FREQ, SIZE, CHAN, BUFFER)
 
 
'''You definitely need test mp3 file (a.mp3 in example) in a directory, say under 'C:\\Temp'
   * To play wav format file instead of mp3, 
      1) replace a.mp3 file with it, say 'a.wav'
      2) In try except clause below replace "playmusic()" with "playsound()"
	
'''

def playSong(filename):
    initMixer()
    print "Play..."
    #playmusic(filename)	
    playsound(filename)

#try:
	
	#filename = '/home/simone/Musica/bass.ogg'
#	playmusic(filename)
#except KeyboardInterrupt:	# to stop playing, press "ctrl-c"
#    stopmusic()
#    print "\nPlay Stopped by user"
#except Exception:
	#print "unknown error"
	
