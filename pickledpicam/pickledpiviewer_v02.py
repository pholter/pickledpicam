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

def serial_init():
    #baudrate =  2457600
    #ser = serial.Serial(port='/dev/ttyAMA0',baudrate = baudrate)
    try:
        ser = serial.Serial(port='/dev/ttyUSB0',baudrate = baudrate)
    except Exception as e:
        print('Could not open serial connection to Pickledpicam',e)
        ser = None

    try:
        serGPS = serial.Serial(port='/dev/ttyACM0',baudrate = 9600)
    except Exception as e:
        print('Could not open serial connection to GPS',e)
        serGPS = None

    return [ser,serGPS]

class pickledpiviewerMainWindow(QtWidgets.QMainWindow):
    def __init__(self,logging_level=logging.INFO,record_folder = None):
        [self.ser,self.serGPS] = serial_init()
        if record_folder == None:
            self.record_folder = os.getcwd()

        self.recording = False
        self.GPS_string = 'NA'
        QtWidgets.QMainWindow.__init__(self)
        mainMenu = self.menuBar()
        self.setWindowTitle("pickledpiviewer")
        # This is the widget with the jpg imageself.GPS_string
        self.imagelabel = QtWidgets.QLabel()
        self.mainwidget = QtWidgets.QWidget()
        self.layout = QtWidgets.QGridLayout(self.mainwidget)
        self.layout.addWidget(self.imagelabel,0,0,1,2)
        # Add a label for the position
        gpslabel = QtWidgets.QLabel('GPS')
        self.poslabel = QtWidgets.QLineEdit('NA')
        self.layout.addWidget(gpslabel,1,0)
        self.layout.addWidget(self.poslabel,1,1)
        # Add a label for the file info
        folderlabel = QtWidgets.QLabel('Folder')
        self.layout.addWidget(folderlabel,2,0)
        self.folderlabel = QtWidgets.QLineEdit(self.record_folder)
        self.layout.addWidget(self.folderlabel,2,1)
        filelabel = QtWidgets.QLabel('File')
        self.layout.addWidget(filelabel,3,0)
        self.filelabel = QtWidgets.QLineEdit('NA')
        self.layout.addWidget(self.filelabel,3,1)
        # Add a record button
        self.record = QtWidgets.QPushButton('Start recording')
        self.record.clicked.connect(self.record_clicked)
        self.layout.addWidget(self.record,4,0,1,2)
        self.setCentralWidget(self.mainwidget)

        quitAction = QtWidgets.QAction("&Quit", self)
        quitAction.setShortcut("Ctrl+Q")
        quitAction.setStatusTip('Closing the program')
        quitAction.triggered.connect(self.close_application)
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(quitAction)

        # Create a timer for reading serial data
        if self.ser is not None:
            self.dread = b''
            self.read_data_timer = QtCore.QTimer()
            self.read_data_timer.timeout.connect(self.read_data)
            self.read_data_timer.start(20)
            self.counter = 0

        if self.serGPS is not None:
            self.gpsread = b''
            self.gps_read_data_timer = QtCore.QTimer()
            self.gps_read_data_timer.timeout.connect(self.read_GPS_data)
            self.gps_read_data_timer.start(250)
        else:
            self.GPS_string = ''


        self.create_filename()
        self.statusBar()
        self.statusBar().showMessage('Welcome!')

    def record_clicked(self):

        s = self.record.text()
        print('Click',s)
        if(s=='Start recording'):
            self.record.setText('Stop recording')
            self.recording = True
        if(s=='Stop recording'):
            self.record.setText('Start recording')
            self.recording = False
    def create_filename(self):
        """ Assembles the filename to save and displays it
        """
        tstr = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.filename = 'pipicam_' + tstr + '__' + self.GPS_string + '.jpg'
        self.filename_full = self.record_folder + '/' + self.filename
        self.filelabel.setText(self.filename)

    def read_GPS_data(self):
        n = self.serGPS.inWaiting()
        if(n > 0):
            data = self.serGPS.read(n)
            #try:
            if True:
                data = data.decode('utf-8')
            print('GPS data',self.gpsread)
            if('$GPGLL' in data):
                ds1 = data.split('$GPGLL')
                dsGPGLL = ds1[1]
                ds2 = dsGPGLL.split('\r\n')
                GPGLL = ds2[0]
                GPS_string = ''
                for l in GPGLL.split(',')[1:6]:
                    GPS_string += l + '_'

                GPS_string = GPS_string[:-1]
                self.GPS_string = GPS_string
                self.poslabel.setText(self.GPS_string)
                self.create_filename()
                print(GPS_string)

    def read_data(self):
        self.counter += 1
        #print('Data!',self.counter,time.time())
        n = self.ser.inWaiting()
        if(n > 0):
            print(self.counter)
            self.dread += self.ser.read(n)
            print('Zeros',self.dread.rfind(b'\x00'))
            ind_zero = self.dread.rfind(b'\x00')
            if(ind_zero > 0):
                ind_zero0 = self.dread[:ind_zero].rfind(b'\x00')
                #print()
                if(ind_zero0 >= 0):
                    print('Received frame',ind_zero0,ind_zero)
                    self.statusBar().showMessage('Received frame')
                    cobs_data = self.dread[ind_zero0+1:ind_zero]
                    try:
                        data = cobs.decode(cobs_data)
                        #print('fsd',self.dread[ind_zero:])
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
                            #stream = io.BytesIO()
                            #stream.write(data)
                            #stream.seek(0)
                            #image = Image.open(stream)
                            #image.show()
                            print(type(data))
                            image = QtGui.QImage()
                            #image = QtGui.QImage.loadFromData(data)
                            image.loadFromData(data)
                            self.imagelabel.setPixmap(QtGui.QPixmap.fromImage(image))
                            # Saving the Data
                            self.create_filename()
                            if(self.recording):
                                f = open(self.filename_full,'wb')
                                f.write(data)
                                f.close()
                                self.statusBar().showMessage('Wrote ' + self.filename_full)


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
