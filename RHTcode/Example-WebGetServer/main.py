import datetime
from bottle import route, request, run, template # $ pip install bottle

temperature = None

@route('/')
def index():

    global token
    global temperature
    token = request.query.token or token
    temperature = request.query.temperature or temperature

	now = datetime.datetime.now()

	f = open(now.strftime('%Y-%m-%d_%H-%M-%S') + '.txt', 'a+')
	f.write('Data: %s\n' % (temperature))
	f.close()

    return template('<b>Temperature: {{temperature}}</b>', temperature=temperature)

run(host='localhost', port=8000)