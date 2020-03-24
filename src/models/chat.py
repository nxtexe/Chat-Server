from common.database import Database
from flask_login import UserMixin
import uuid

class Chat(UserMixin):
	def __init__(self, _id, user, chats=[]):
		self._id = _id
		self.chats = chats
		self.user = user

	def get_id(self):
		return self._id

	def append_chat(self, chat):
		"""query={"email": email}, new_val={"$set": {"password": password}} """
		self.chats.append(chat)
		Database.update(collection="chats", query={"_id": self._id}, new_val={"$set": {"chats": self.chats}})

	@classmethod
	def get_all(cls):
		chats = Database.find(collection="chats", query=({}))
		return [cls(**chat) for chat in chats]

	@classmethod
	def get_by_id(cls, _id):
		data = Database.find_one(collection="chats", query={ "_id": _id })
		if data is not None:
			return cls(**data)


	def json(self):
		return {
			"_id": self._id,
			"chats": self.chats,
			"user": self.user
		}

	def save_to_mongo(self):
		Database.insert(collection="chats", data=self.json())