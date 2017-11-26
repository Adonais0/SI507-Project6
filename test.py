import json
import csv
def csv_to_dict_list(csvFile):
    f = csv.reader(open(csvFile,'r'))
    next(f)
    i = 1
    list_of_dict = []
    for row in f:
        row.insert(0,i)
        i = i+1
        row[3], row[2] = row[2], row[3]
        row.insert(3,"state_id")#to be modified later
        del row[-2]

        dict_of_csv = {}
        dict_of_csv['id'] = row[0]
        dict_of_csv['name'] = row[1]
        dict_of_csv['type'] = row[2]
        dict_of_csv['state_id'] = row[3]
        dict_of_csv['location'] = row[4]
        dict_of_csv['description'] = row[5]
        list_of_dict.append(dict_of_csv)
    return list_of_dict
print(csv_to_dict_list('arkansas.csv'))

def csv_to_name_dict(csvFile):
    f = csv.reader(open(csvFile,'r'))
    next(f)
    i = 1
    list_of_dict = []
    for row in f:
        row.insert(0,i)
        i = i+1
        row[3], row[2] = row[2], row[3]
        del row[-2]
        dict_of_csv = {}
        dict_of_csv['id'] = row[0]
        dict_of_csv['name'] = row[1]
        list_of_dict.append(dict_of_csv)
    return list_of_dict
print(csv_to_name_dict('arkansas.csv'))
    # if key in result:
        # implement your duplicate row handling here

        #switch row[1] and row[2]

        # pass
    # result[key] = row[1:]
# print (result.keys())
