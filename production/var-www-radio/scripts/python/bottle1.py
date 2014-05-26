from bottle import route, run, template

isActive = False

@route('/')
def index():
    global isActive
    print(isActive)
    h = hello()
    return h

@route('/bar')
def index():
    global isActive
    isActive = True
    return 'yo'

@route('/foo')
def index(name = 'time'):
    return template('<p>Hello, world</p>')

def hello():
    return 'hello, world'


run(host='localhost', port=8080)


