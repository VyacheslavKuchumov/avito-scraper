from pymongo import MongoClient

client = MongoClient("localhost", 27017)

db = client.jobData

job_collection = db.jobs