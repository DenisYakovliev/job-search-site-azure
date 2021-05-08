import os
import time
import random

file = open('tmp_file.txt', 'w+')
user_counts = 50
job_per_user = 10

specialty = [
    {"Python": [[['Junior', 500], ['Middle', 1500], ['Senior', 4000]], ['Full time', 'Part time'], ["Web developer", "Software Developer"]]},
    {"Java": [[['Junior', 400], ['Middle', 1500], ['Senior', 3500]], ['Full time', 'Part time'], ["Web developer", "Software Developer"]]},
    {'QA': [[['Junior', 300], ['Middle', 1000], ['Senior', 2000]], ['Full time', 'Part time'], ["Software Developer"]]},
    {'c#/.NET':[[['Junior', 400], ['Middle', 1500], ['Senior', 3500]], ['Full time', 'Part time'], ["Web developer", "Software Developer"]]},
    {'C/C++ Embedded': [[['Junior', 500], ['Middle', 1500], ['Senior', 4000]], ['Full time', 'Part time'], ["Software Developer"]]},
    {'Project Manager': [[['Junior', 400], ['Middle', 1200], ['Senior', 3000]], ['Full time', 'Part time'], ["Web developer", "Software Developer"]]},
    {'Designer': [[['Junior', 300], ['Middle', 10000], ['Senior', 2500]], ['Full time', 'Part time'], ["Graphic design", "Web design"]]},
    {'HR': [[['Junior', 300], ['Middle', 1500], ['Senior', 4000]], ['Full time', 'Part time'], ["Human Resources"]]},
    {'Data Scientist': [[['Junior', 700], ['Middle', 3000], ['Senior', 5000]], ['Full time', 'Part time'], ["Software Developer"]]},
]

locations = [
    'Kharkiv',
    'Kiev',
    'Lviv',
    'Odessa',
]

for i in range(user_counts):
    if i % 2 != 0:
        for j in range(job_per_user):
            sp = random.choice(specialty)
            key = sp.keys()[0]
            data = sp[key]
            sp_0 = random.choice(data[0])
            sp_1 = 'Internship' if sp_0[0] == 'Junior' else random.choice(data[1])
            sp_2 = random.choice(data[2])
            
            title = "'" + sp_0[0] + ' ' + key + ' ' + sp_2 + "'"
            salary = sp_0[1]
            location = "'" + random.choice(locations) + "'"
            type = "'" + sp_1 + "'"
            category = "'" + sp_2 + "'"
            website = "'" + "www.my-company.com" + "'"
            filled = 0
            views = 1
            user_id = i 
            price = salary * 0.05 
            description = title
            
            finaly_data = [title,
                           str(salary),
                           location,
                           type,
                           category,
                           'GETDATE()',
                           website,
                           'GETDATE()',
                           str(filled),
                           str(views),
                           str(user_id),
                           str(price),
                           description]
            job_string = "( " + ", ".join(finaly_data) + " )" + ",\n"
            file.write(job_string)
