#!/usr/bin/python
# Copyright 2015 Manylabs - MIT License
# Author: Elliott Dicus
#
# Script to respond to authorization requests from an Arduino powered RFID
# reader

import os
import serial
import time
import urllib
import urllib2
import logging
from datetime import datetime

DEBUG = True # Set to True to print info to std out

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SERIAL_PORT = "/dev/ttyACM0"

idFile = "/home/pi/rfid/access_control/ids.csv"
accessLog = "/home/pi/rfid/access_control/accessLog.csv"

def watchForReport( port ):
    reportString = ''

    if DEBUG:
        print "Ready"

    # Start read loop
    while True:

        data = port.read()

        # Look for opening ('\x02') and closing bytes ('\x03'), otherwise store
        # the byte as long as it's not empty
        if data == '\x02':

            # Reset
            reportString = ''
        elif data == '\x03':
            if DEBUG:
                print "Checking ID -", # Comma because we don't want a newline

            direction, cardId = reportString.split(":")

            if DEBUG:
                print "ID: %s" % cardId

            # Reset
            reportString = ''

            processId( port, cardId, direction )

        elif data is not '':
            reportString += data

def processId( port, cardId, direction ):
    name =  findNameForId( cardId )
    if name:

        # Record success
        recordAccess( cardId, direction, name, "Success: open strike" )

        # Respond to arduino
        port.write('\x02allowed\x03')

        # Let slack know
        logger.info('slack posting in progress...')
        slackParams = { 
	        'token' : 'xoxp-4031269372-4894232517-19749775430-08f5b4ab7f',
	        'channel' : '#door',
	        'text' : direction + ' ' + name,
	        'username' : 'doorbot'
        }
        urllib2.urlopen('https://slack.com/api/chat.postMessage?' + urllib.urlencode(slackParams))
        logger.info('slack posting done.')
    else:

        # Record failure
        recordAccess( cardId, direction, detail="Failure: ID does not have access" )

        # Respond to arduino
        port.write('\x02denied\x03')

def findNameForId( decodedId ):
    with open( idFile, 'r', os.O_NONBLOCK ) as f:
        for line in f:

            # Ignore blank and commented lines
            if line and not line.startswith( "#" ):

                # Separate values
                cardId, name = [v.strip() for v in line.split( "," )]

                # Make sure to compare strings
                if cardId == str(decodedId):
                    return name
    return None

def recordAccess(cardId="", direction="", name="", detail=""):
    with open( accessLog, 'a', os.O_NONBLOCK ) as f:

        # TODO: Record Survey responses

        # Lines are in the following format:
        # Timestamp, CardId, Direction, Name, Detail
        line = "%s, %s, %s, %s, %s\n" % ( str(datetime.now()), cardId, direction, name, detail )

        if DEBUG:
            print line

        f.write( line )
        f.flush()


def sigterm_handler(_signo, _stack_frame):
    "When sysvinit sends the TERM signal, cleanup before exiting."
    print("[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] received signal {}, exiting...".format(_signo))

    sys.exit(0)

if __name__ == "__main__":

    # Open Serial Port
    portOpen = False
    while not portOpen:
        try:
            port = serial.Serial( SERIAL_PORT, baudrate=9600, timeout=0 )
            portOpen = True
        except serial.SerialException as e:
            print "Could not open serial port. Trying again in 5 seconds."
            portOpen = False
            time.sleep(5)

    # Start read loop
    try:
        watchForReport( port )
    except KeyboardInterrupt as e:
        pass
    except serial.SerialException as e:
        print "Serial port disconnected. Quitting."
