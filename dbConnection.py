from pymongo import MongoClient

client = MongoClient("localhost", 27017)

db = client.jobData

jobUrl_collection = db.jobUrls
job_collection = db.jobs