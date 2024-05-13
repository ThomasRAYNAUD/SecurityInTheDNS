import csv

with open("./school_websites.csv", "r", encoding='utf-8') as f:
    reader = csv.reader(f, delimiter = ",")
    school_dict = {}
    reader.__next__()

    for ligne in reader:
        name = ligne[0]
        web = ligne[6]
        if name not in school_dict :
            school_dict[name] = web
        elif school_dict[name] != web :
            school_dict[name+"2"] = web
