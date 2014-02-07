import pygame
import os
import sys
import json
import thread
import time
import eyed3
import httplib
from httplib2 import Http

class TrackMasterPlayer():

	def __init__(self,path):
		self.soundfile = []
		self.path = path

	def listFiles(self,path):
	    fileList = []
	    rootdir = path
	    for root, subFolders, files in os.walk(rootdir):
	        for file in files:
	            if file.endswith('.mp3'):
	                fileList.append(os.path.join(root,file))
	    return fileList

	def readTag(self,path):
	    audiofile = eyed3.load(path)
	    data = {
	        'title': audiofile.tag.title,
	        'author': audiofile.tag.artist,
	        'album': audiofile.tag.album,
	        'path': path,
	        'genre': "genre"
	    }
	    return data

	def getData(self,path):
	    data = {}
	    files = self.listFiles(path)
	    i = 0
	    for file in files:
	        if file.endswith('.mp3'):
	        	singleSong = self.readTag(file)
	        	data["song"+str(i)] = singleSong
	        	i = i+1
	    return data

	def synchMusic(self):
	    myData = self.getData(self.path)
	    http_obj = Http()
	    http_obj.request(uri='http://localhost/blackbox-rest/app-rest/synch',method='POST',headers={'Content-Type': 'application/json; charset=UTF-8'}, body=json.dumps(myData),)
	    print json.dumps(myData)
	    return json.dumps(myData)

	def getNext(self):
	    conn = httplib.HTTPConnection("127.0.0.1")
	    conn.connect()
	    conn.request("GET", "/blackbox-rest/app-rest/next")
	    r1 = conn.getresponse()
	    s = r1.read()
	    a = json.loads(s)
	    self.soundfile = a


	def playmusic(self):
		clock = pygame.time.Clock()
		pygame.mixer.music.load(self.soundfile['Path'])
		print "Start Playing " + self.soundfile['Title']
		pygame.mixer.music.play()
		pygame.mixer.music.set_endevent(pygame.USEREVENT)
		quit = False
		while not quit:
			clock.tick(30)
			for event in pygame.event.get():
				if event.type == pygame.USEREVENT:
					print self.soundfile['Title'] + " Finish"
					quit = True
		self.startPlay()

	def startPlay(self):
		#pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
		pygame.init()
		pygame.mixer.init()
		self.getNext()
		self.playmusic()

	def stopmusic(self):
		pygame.mixer.music.stop()


a = TrackMasterPlayer("/home/simone/Musica")
a.synchMusic()
a.startPlay()
	 

	