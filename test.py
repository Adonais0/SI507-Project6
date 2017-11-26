import json
import csv
def csv_to_dict_list(csvFile,i):
    f = csv.reader(open(csvFile,'r'))
    next(f)
    list_of_dict = []
    for row in f:
        row.insert(0,i)
        i = i+1
        row[3], row[2] = row[2], row[3]
        del row[-2]

        dict_of_csv = {}
        dict_of_csv['id'] = row[0]
        dict_of_csv['name'] = row[1]
        dict_of_csv['type'] = row[2]
        dict_of_csv['location'] = row[3]
        dict_of_csv['description'] = row[4]
        list_of_dict.append(dict_of_csv)
    return list_of_dict

dict_list = []
ar_dict_list = csv_to_dict_list('arkansas.csv',1)
print(len(ar_dict_list))
mi_dict_list = csv_to_dict_list('michigan.csv',len(ar_dict_list)+1)
print(len(ar_dict_list)+len(mi_dict_list))
ca_dict_list = csv_to_dict_list('california.csv',16)
for d in ar_dict_list:
    dict_list.append(d)
for d in mi_dict_list:
    dict_list.append(d)
for d in ca_dict_list:
    dict_list.append(d)
print(dict_list)
for a in dict_list:
    print(a['id'])
    # if key in result:
        # implement your duplicate row handling here

        #switch row[1] and row[2]

        # pass
    # result[key] = row[1:]
# print (result.keys())
