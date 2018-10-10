#!flask/bin/python
from application import application, socketio

if __name__ == '__main__':
	socketio.run(application, host="0.0.0.0", debug=True)