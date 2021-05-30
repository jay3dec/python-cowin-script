import requests
import json
from win10toast import ToastNotifier
import datetime
from datetime import date 
from pygame import mixer
import time

toaster = ToastNotifier()
PIN_CODE = 689586

def loadCowinData():
    today = date.today()
    fromDate = today.strftime("%d-%m-%Y")

    print "#############################################"
    
    print "Checking vaccine availablity for pincode " + str(PIN_CODE) + " on date " + fromDate
    API_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode="+str(PIN_CODE)+"&date="+fromDate	
    resp = requests.get(API_URL)
    return resp.content

def playSong():
    '''
    utility function to play song
    '''
    mixer.init()
    mixer.music.load("song.mp3")
    mixer.music.set_volume(10)
    mixer.music.play()

def parseJSON(res):
    '''
    utility function to parse API JSON response
    '''
    root = json.loads(res);
    centres = root['centers']
    if len(centres) == 0:
        return "No centres found !!" 
    else:
        return checkVaccineAvailabilty(centres)

def checkVaccineAvailabilty(centres):
    '''
    utility function to check for vaccine availablity
    '''
    for center in centres:
        block = center['block_name']
        for session in center['sessions']:
            if session['min_age_limit'] == 18 and session['available_capacity'] > 0:
                print currentDateTime() + "FOUND ONE"
                return str(session['available_capacity']) + ' doses of ' + session['vaccine'] + ' available @ ' + block
    
    print currentDateTime() + ' :: None found in ' + block + '. Checking in a minute ...'
    print "#############################################"
    print "---------------------------------------------"
    return 'None'    

def currentDateTime():
    '''
    utility function to get current date and time
    '''
    return datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S")

def showNotification(message):
    '''
    utility method to show desktop notification 
    '''
    toaster.show_toast("Cowin Notification",
    message,
    icon_path="custom.ico",
    duration=30)

def main():
    '''
    the main function 
    '''
    response = loadCowinData()
    vaccine_available = parseJSON(response)
    if vaccine_available != 'None':
        playSong()
        showNotification(vaccine_available)
        
    time.sleep(40)

#######################################################################
#################### THIS IS WHERE IT ALL STARTS ######################
#######################################################################
while True:
    main()