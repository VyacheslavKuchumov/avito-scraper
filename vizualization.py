import pandas
from dbConnection import jobs_collection


df = pandas.DataFrame(list(jobs_collection.find({})))

fields = []
for field in df['fieldOfExp']:
    try:
        fields.index(field)
    except ValueError:
        fields.append(field)



print(fields)

