import pygame
import os
import sys
import json
import threading
import time
import eyed3
import httplib
from httplib2 import Http

on = 0
start = 0

class TrackMasterPlayer(threading.Thread):

    def __init__(self,path):
        threading.Thread.__init__(self)
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
        self.getNext()
        pygame.mixer.music.load(self.soundfile['Path'])
        print "Start Playing " + self.soundfile['Title']
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

    def initPlayer(self):
        pygame.init()
        pygame.mixer.init()
        
        #self.playmusic()

    def stopmusic(self):
        pygame.mixer.music.stop()

    def run(self):
        time.sleep(3)
        global on
        global start
        self.clock = pygame.time.Clock()
        self.initPlayer()
        if on and start:
            self.clock.tick(30)
            print "...PLAYING..."
            self.playmusic()
            quit = False
            while not quit:
                if not start or not on:
                    print "Playing Stopped"
                    pygame.mixer.music.stop()
                    quit = True
                else: 
                    self.clock.tick(30)
                    for event in pygame.event.get():
                            if event.type == pygame.USEREVENT:
                                print self.soundfile['Title'] + " Finish"
                                quit = True
            self.run()
        else:
            time.sleep(1)
            self.run()
        
        """
        if(on):
            self.startPlay()
            quit = False
            while not quit:
                self.clock.tick(30)
                if on == 0:
                    print "Playing Stopped"
                    pygame.mixer.music.stop()
                    quit = True
                else:
                    for event in pygame.event.get():
                        if event.type == pygame.USEREVENT:
                            print self.soundfile['Title'] + " Finish"
                            quit = True
            self.startPlay()
        """
            
                                                          


class StopMusic(threading.Thread):
    
    def __init__(self):
        
        threading.Thread.__init__(self)

    
    def run(self):
        global on
        global start
        if(on):
            time.sleep(10)
            on = 0
            start = 0
            print "Stop Playing"
        else:
            time.sleep(1)
            self.run()

class StartMusic(threading.Thread):
    
    def __init__(self):
        
        threading.Thread.__init__(self)

    
    def run(self):
        global on
        global start
        if(not on):
            time.sleep(1)
            on = 1
            start = 1
            print "Start Playing"
        else:
            time.sleep(1)
            self.run()


t1 = TrackMasterPlayer("/home/simone/Musica")
t2 = StopMusic()
t3 = StartMusic()
t1.start()
#t2.start()
t3.start()
t1.join()
#t2.join()
t3.join()

"""
a = TrackMasterPlayer("/home/simone/Musica")
a.synchMusic()
a.startPlay()
"""