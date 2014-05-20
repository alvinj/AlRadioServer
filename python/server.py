from bottle import route, run, template

import si4703
fm = si4703.si4703()
isOn = False

@route('/')
def index():
    return 'yo'

@route('/tune/<station>')
def tune(station = '104.3'):
    global isOn
    if isOn == False:
        fm.init()
        isOn = True
    fm.tune(station)
    return "would have tuned to " + station

@route('/turn_off')
def turn_off():
    global isOn
    isOn = False
    fm.turn_off()
    return 'turned off'

@route('/set_volume/<volume>')
def set_volume(volume = '10'):
    fm.volume(volume)
    return 'volume = ' + volume

run(host='localhost', port=5151)


