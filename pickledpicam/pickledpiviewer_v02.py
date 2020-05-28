import sys
import os
import logging
import argparse
import time
import locale
import pkg_resources
import datetime
import numpy as np
import serial
from cobs import cobs
import io
from PIL import Image
import struct
#from pytz import timezone

try:
    from PyQt5 import QtCore, QtGui, QtWidgets
except:
    from qtpy import QtCore, QtGui, QtWidgets

baudrate = 614400 # works
#baudrate =   921600 # works
baudrate = 230400 # works
baudrate = 345600
#baudrate = 9600
baudrate = 1228800
#baudrate =  2457600
#ser = serial.Serial(port='/dev/ttyAMA0',baudrate = baudrate)
ser = serial.Serial(port='/dev/ttyUSB0',baudrate = baudrate)

class pickledpiviewerMainWindow(QtWidgets.QMainWindow):
    def __init__(self,logging_level=logging.INFO):
        QtWidgets.QMainWindow.__init__(self)
        mainMenu = self.menuBar()
        self.setWindowTitle("pickledpiviewer")
        self.imagelabel = QtWidgets.QLabel()
        self.mainwidget = self.imagelabel
        self.setCentralWidget(self.mainwidget)
        
        quitAction = QtWidgets.QAction("&Quit", self)
        quitAction.setShortcut("Ctrl+Q")
        quitAction.setStatusTip('Closing the program')
        quitAction.triggered.connect(self.close_application)
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(quitAction)

        # Create a timer for reading serial data
        self.dread = b''
        self.read_data_timer = QtCore.QTimer()
        self.read_data_timer.timeout.connect(self.read_data)
        self.read_data_timer.start(20)
        self.counter = 0
        
        
        self.statusBar()

    def read_data(self):
        self.counter += 1
        print('Data!',self.counter,time.time())
        n = ser.inWaiting()
        if(n > 0):
            print(self.counter)
            self.dread += ser.read(n)
            print('Zeros',self.dread.rfind(b'\x00'))
            ind_zero = self.dread.rfind(b'\x00')
            if(ind_zero > 0):
                ind_zero0 = self.dread[:ind_zero].rfind(b'\x00')
                #print()
                if(ind_zero0 >= 0):
                    print('Found frame',ind_zero0,ind_zero)
                    cobs_data = self.dread[ind_zero0+1:ind_zero]
                    try:
                        data = cobs.decode(cobs_data)
                        print('fsd',self.dread[ind_zero:])
                        self.dread = self.dread[ind_zero:]
                        if(len(data) > 10):
                            # Check if we have a package
                            package = data[0]
                            pictime = data[1:9]
                            print(data[0:10])
                            tu = struct.unpack('d',pictime)[0]
                            print('Package',package)
                            print('time',tu)
                            data = data[9:]
                            print('Opening image')
                            stream = io.BytesIO()
                            stream.write(data)
                            stream.seek(0)
                            #image = Image.open(stream)
                            #image.show()
                            print(type(data))
                            image = QtGui.QImage()
                            #image = QtGui.QImage.loadFromData(data)
                            image.loadFromData(data)
                            self.imagelabel.setPixmap(QtGui.QPixmap.fromImage(image))
                    except Exception as e:
                        print(e)


    def close_application(self):
        sys.exit()                                



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = pickledpiviewerMainWindow()
    w = 1000
    h = 600
    window.resize(w, h)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()    
