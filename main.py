from flask import Flask,render_template,request,redirect,url_for,session
from flask_socketio import SocketIO,send,emit,leave_room,join_room
from flask_session import Session
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/cipl/Desktop/sockeio_chat/static'
app = Flask(__name__)
socketio = SocketIO(app)
app.config['SICKRET_KEY'] = "SECRECT"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Session(app)

socketio = SocketIO(app,manage_session = False)
@app.route('/', methods=['GET','POST'])
def index():

    return render_template('index.html')
@app.route('/chat',methods=['GET','POST'])
def chat():
    if(request.method=='POST'):
        username = request.form['username']
        room = request.form['room']
        session['username'] = username
        session['room'] = room
        return render_template('chat.html',session=session)
    else:
        if(session.get('username') is not None):
            return render_template('chat.html',session=session)
        else:
            return redirect(url_for('index'))

@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=room)






@socketio.on('message')
def handle_message(message):
	print("received message" + message)
	send(message,broadcast=True)

@socketio.on('image')
def handle_image(image_data,):


    print('recieved image data'+ image_data)

    emit('image',image_data,broadcast=True)







if __name__ == '__main__':
    app.debug=True
    socketio.run(app,host='0.0.0.0')
