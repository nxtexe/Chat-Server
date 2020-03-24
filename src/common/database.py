import os
import pymongo
import urllib

class Database():
	#URI = "mongodb+srv://" + os.getenv('MONGO_USERNAME') + ":"+ urllib.parse.quote(os.getenv('MONGO_PASSWORD')) + "@cluster0-ln3eh.mongodb.net/test?retryWrites=true&w=majority"
	DATABASE = None

	@staticmethod
	def initialize(username, password):
		client = pymongo.MongoClient("mongodb+srv://" + username + ":"+ urllib.parse.quote(password) + "@cluster0-ln3eh.mongodb.net/test?retryWrites=true&w=majority")
		Database.DATABASE = client['Nxte']

	@staticmethod
	def insert(collection, data):
		Database.DATABASE[collection].insert(data)

	@staticmethod
	def find(collection, query):
		return Database.DATABASE[collection].find(query)

	@staticmethod
	def search(collection, qs):
		query = {"$text": {"$search": qs }} 
		return Database.DATABASE[collection].find(query)

	@staticmethod
	def find_one(collection, query):
		return Database.DATABASE[collection].find_one(query)


	@staticmethod
	def remove(collection, data):
		Database.DATABASE[collection].remove(data)


	@staticmethod
	def update(collection, query, new_val):
		"""query={"email": email}, new_val={"$set": {"password": password}} """
		Database.DATABASE[collection].update_one(query, new_val)
