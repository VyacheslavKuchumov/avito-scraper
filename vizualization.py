import pandas
from dbConnection import jobs_collection


df = pandas.DataFrame(list(jobs_collection.find({})))

fields = []
for field in df['fieldOfExp']:
    try:
        fields.index(field)
    except ValueError:
        fields.append(field)


fieldCount = {field: 0 for field in fields}
for field in df['fieldOfExp']:
    fieldCount[field] +=1

