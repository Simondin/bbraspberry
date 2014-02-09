import pygame
import os
import sys
import json
import threading
import time
import eyed3
import httplib
from httplib2 import Http
from LCD.Adafruit_CharLCDPlate import Adafruit_CharLCDPlate


class TrackMasterPlayer(threading.Thread):

    def __init__(self,path):
        threading.Thread.__init__(self)
        self.soundfile = []
	self.title = "Happy"
	self.canzone = path + "happy.mp3"
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
        """conn = httplib.HTTPConnection("127.0.0.1")
        conn.connect()
        conn.request("GET", "/blackbox-rest/app-rest/next")
        r1 = conn.getresponse()
        s = r1.read()
        a = json.loads(s)
        self.soundfile = a"""

    def initPlayer(self):
        pygame.init()
        pygame.mixer.init()

    def playMusic(self):
        self.getNext()
        pygame.mixer.music.load(self.canzone)
        print "Start Playing " + self.title
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.USEREVENT) 


    def stopMusic(self):
        pygame.mixer.music.stop()

    def run(self):
        time.sleep(3)
        global on
        global lcd
        global start
        self.initPlayer()
        self.clock = pygame.time.Clock()
        if on :
            if start:
                self.clock.tick(30)
                print "...PLAYING..."
                lcd.clear()
                lcd.message("ON AIR \n"+self.title)
                self.playMusic()
                quit = False
                while not quit:
                    if not start or not on:
                        print "Playing Stopped"
                        self.stopMusic()
                        quit = True
                    else: 
                        self.clock.tick(30)
                        for event in pygame.event.get():
                                if event.type == pygame.USEREVENT:
                                    print self.title + " Finish"
                                    quit = True
                self.run()
            else:
                time.sleep(1)
                self.run()

        else:
            return
                                                          


class StopMusic(threading.Thread):
    
    def __init__(self):
        
        threading.Thread.__init__(self)

    
    def run(self):
        global on
	global lcd
	global start
	btn = lcd.LEFT
	while True:
            if on :
                if start:
                    if lcd.buttonPressed(btn):
                	lcd.clear()
			lcd.message("Stop Music")
		        print "Stop Playing"
			start = 0
                else:
                    time.sleep(1)
            else:
                return
       

class StartMusic(threading.Thread):
    
    def __init__(self):
        
        threading.Thread.__init__(self)

    
    def run(self):
        global on
        global start
	global lcd
	btn = lcd.RIGHT
	while True:
            if on :
                if not start :
                    if lcd.buttonPressed(btn):
                        lcd.clear()
                        lcd.message("Start Music")
                        print "Start Music"
                        start = 1
                else:
                    time.sleep(1)
            else:
                return

class Switchoff(threading.Thread):
    
    def __init__(self):
        
        threading.Thread.__init__(self)

    
    def run(self):
        global on
	global lcd
	btn = lcd.SELECT
	while True:
            if on :
	    	if lcd.buttonPressed(btn):
                    start = 0
                    on = 0
                    time.sleep(1)
                    lcd.clear()
                    lcd.message("Switch Off...")
		    print "Switch off..."
		    time.sleep(2)
		    lcd.clear()
		    lcd.backlight(lcd.OFF)
		    return
            else:
                time.sleep(1)



class Switchon(threading.Thread):
    
    def __init__(self):
        
        threading.Thread.__init__(self)

    
    def run(self):
        global on
	global lcd
	global start
        lcd.clear()
        lcd.message("...BOOTING...")
        print "...Booting..."
        on = 1
        start = 0
        time.sleep(3)
        lcd.clear()
        lcd.message("Synchronize Now?")
        ready = False
        while not ready:
            if lcd.buttonPressed(lcd.RIGHT):
                lcd.clear()
                lcd.message("Synch...")
                print "Synch..."
                time.sleep(2)
                ready = True
                
            if lcd.buttonPressed(lcd.LEFT):
                ready = True
                
        lcd.clear()
        lcd.message("Ready!")
        print "Ready"

        t1 = TrackMasterPlayer("/home/pi/bbraspberry/test-file/")
        t2 = StopMusic()
        t3 = StartMusic()
        t4 = Switchoff()

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        
on = 0
start = 0
lcd = Adafruit_CharLCDPlate(busnum = 1)
t = Switchon()
t.start()
t.join()


"""
a = TrackMasterPlayer("/home/simone/Musica")
a.synchMusic()
a.startPlay()
"""
