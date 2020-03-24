from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS, cross_origin
from common.database import Database 
from dotenv import load_dotenv
from models.chat import Chat
from flask import Flask
import requests
import os


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
login_manager = LoginManager()
login_manager.init_app(app)
io = SocketIO(app, cors_allowed_origins="*")

# @app.before_first_request
# def initialize():
# 	Database.initialize(os.getenv("MONGO_USERNAME"), os.getenv("MONGO_PASSWORD"))

Database.initialize(os.getenv("MONGO_USERNAME"), os.getenv("MONGO_PASSWORD"))

@login_manager.user_loader
def load_user(user_id):
	return Chat.get_by_id(user_id)


@io.on('connect', namespace="/chat")
def connect():
	print("Established connection")

@io.on('disconnect', namespace="/chat")
def disconnect():
	print("Connection terminated.")
	logout_user()

@io.on('register', namespace="/chat")
def register(json):
	user = Database.find_one(collection="users", query={ "_id": json[0] })
	if user is not None:
		chat = Chat.get_by_id(json[0])
		if chat is None:
			user["authenticated"] = True
			chat = Chat(_id=message, user=user)
			chat.save_to_mongo()
			join_room(chat._id)
			login_user(chat)
		else:
			join_room(chat._id)
			login_user(chat)
	else:
		#raise ConnectionRefusedError('unauthorized!')
		pass

@io.on('send_chat', namespace="/chat")
def send(json):
	for recepient in json["transportIDs"]["reciever"]:
		emit("chat", json,  room=recepient)
		json["status"] = "sent"
		chat = Chat.get_by_id(recepient)
		chat.append_chat(json)
	return json

@io.on('typing', namespace="/chat")
def typing(json):
	emit("typing", room=current_user.get_id())

if __name__ == "__main__":
	io.run(app, debug=True, host='localhost', port='8000')