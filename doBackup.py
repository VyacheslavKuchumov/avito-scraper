from dbConnection import client
import pandas

data = client.jobData.jobs.find({})





client.Analytics.jobs.insert_many(data)
