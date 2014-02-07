#!/usr/bin/python
# Importiamo le librerie per l'interfaccia grafica GTK
import pygtk
pygtk.require('2.0')
import gtk
import thread
import play
import os
import sys
import json
import thread
import time
import eyed3
import httplib
from httplib2 import Http

#questa e' la classe che definisce l'interfaccia grafica
class Dialogo:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)  # definiamo la finestra
        self.window.set_title("Master Track")# le diamo in titolo
        self.window.connect("destroy", self.distruggi) # catturiamo l'evento destroy 
                                                       #(es. la X che chiude la finestra)
                                                       # e lo indirizziamo a una funzione
                                                       # che termina il programma
        self.window.set_resizable(True)            # la finestra non e' modificabile in dimensioni
        self.window.set_position(gtk.WIN_POS_MOUSE)
        self.path = gtk.Entry()
        self.path.set_text("/home/simone/Musica")



        self.synch = gtk.Button("Sincronizza Cartelle")
        self.synch.connect("clicked", self.synchMusic)

        self.start = gtk.Button("Start")
        self.start.connect("clicked", self.playMusic)

        self.stop = gtk.Button("Stop")
        self.stop.connect("clicked", self.stopMusic)                                             # e compare nell'attuale posizione del muose
        
        self.etichetta = gtk.Label("Canzone...")   # testo che richiede la lunghezza del 1 lato
        self.canzone = gtk.Label()
        self.colonna = gtk.VBox()          # creiamo un contenitore dove 
                                           # gli oggetti sono disposti in verticale (una colonna)
        self.colonna.pack_start(self.path)
        self.colonna.pack_start(self.synch)
        self.colonna.pack_start(gtk.Label())
        self.colonna.pack_start(self.etichetta)
        self.colonna.pack_start(self.canzone)
        self.colonna.pack_start(self.start)
        self.colonna.pack_start(self.stop)
        self.window.add(self.colonna)  # inseriamo il tutto nella finestra
        self.window.show_all()         # comando che visualizza la finestra ed il suo contenuto
    
    # funzione di uscita
    def distruggi(self, widget,data = None):
        print data
        return gtk.main_quit()
    # funzione di lancio della GUI
    def main(self):
        gtk.main()


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

    def synchMusic(self,widget):
        path = self.path.get_text()
        myData = self.getData(path)
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
        return a

    def stopMusic(self,widget):
        play.stopmusic()

    def playMusic(self,widget):
        #data = self.getNext()
        #self.canzone.set_text(data['Title'])
        
        play.playSong("/home/pi/bbraspberry/test-file/01-red-intro.mp3")   
	
          

# avvio del programma a condizione che non sia caricato come modulo
print __name__
if __name__ == "__main__":
    base = Dialogo()
    base.main()
