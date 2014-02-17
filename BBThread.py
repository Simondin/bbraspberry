import pygame
import os
import sys
import json
import threading
import time
from hsaudiotag import auto
import httplib
from httplib2 import Http
from LCD.Adafruit_CharLCDPlate import Adafruit_CharLCDPlate


class TrackMaster():

    def __init__(self):
        self.soundfile = []
        self.path = "/media/LEXAR/TrackMaster"
	pygame.init()
        pygame.mixer.init()
	pygame.mixer.music.set_volume(1.00)

    def listFiles(self):
        fileList = []
        rootdir = self.path
        for root, subFolders, files in os.walk(rootdir):
            for file in files:
                if file.endswith('.mp3'):
                    fileList.append(os.path.join(root,file))
        return fileList

    def readTag(self,file):
        audiofile = auto.File(file)
        data = {
            'title': audiofile.title,
            'author': audiofile.artist,
            'album': audiofile.album,
            'path': file.split("/TrackMaster")[-1],
            'genre': audiofile.genre,
            'durata': audiofile.duration,
        }
        return data

    def getData(self):
        data = {}
        files = self.listFiles()
        i = 0
        for file in files:
            if file.endswith('.mp3'):
                singleSong = self.readTag(file)
                data["song"+str(i)] = singleSong
                i = i+1
        return data

    def synchMusic(self):
        myData = self.getData()
	print json.dumps(myData)
        http_obj = Http()
        http_obj.request(uri='http://blackbox-rest.gopagoda.com/app-rest/synch',method='POST',headers={'Content-Type': 'application/json; charset=UTF-8'}, body=json.dumps(myData),)
        return json.dumps(myData)

    def getNext(self):
        conn = httplib.HTTPConnection("blackbox-rest.gopagoda.com")
        conn.connect()
        conn.request("GET", "/app-rest/next")
        r1 = conn.getresponse()
        s = r1.read()
        a = json.loads(s)
        self.canzone = a       

    def playMusic(self):
        self.getNext()
        pygame.mixer.music.load(self.path + self.canzone['Path'])
        print "Start Playing " + self.canzone['Title']
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.USEREVENT) 


    def stopMusic(self):
        pygame.mixer.music.stop()


class Player(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global on
        global lcd
        global start
	global track_master
        self.clock = pygame.time.Clock()
        if on :
            if start:
                self.clock.tick(30)
                print "...PLAYING..."
		track_master.playMusic()
                lcd.clear()
		lcd.message("ON AIR \n"+track_master.canzone['Title'])
                quit = False
                while not quit:
                    if not start or not on:
                        print "Playing Stopped"
                        track_master.stopMusic()
                        quit = True
                    else: 
                        self.clock.tick(30)
                        for event in pygame.event.get():
                                if event.type == pygame.USEREVENT:
                                    print track_master.canzone['Title'] + " Finish"
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
	global track_master
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
		track_master.synchMusic()
                time.sleep(2)
                ready = True
                
            if lcd.buttonPressed(lcd.LEFT):
                ready = True
                
        lcd.clear()
        lcd.message("Ready!")
        print "Ready"

        t1 = Player()
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
track_master = TrackMaster()
lcd = Adafruit_CharLCDPlate(busnum = 1)
t = Switchon()
t.start()
t.join()
