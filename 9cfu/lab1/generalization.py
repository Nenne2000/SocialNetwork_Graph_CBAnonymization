import csv
import pandas as pd
from faker import Faker
class Tree:

    data = []
    level = 0
    parent = {}

    def __init__(self, l):
        self.level = l

    def connect(self, n, p):
        self.parent[n] = p # definisco il parent di un nodo

    def generalize(self, n):
        return self.parent[n] # restituisco il parent (valore più generale di n)

age = Tree(4)
zip = Tree(5)

with open("age.csv", "r") as f:
    for row in csv.DictReader(f):
        L0 = int(row["L0"])
        L1 = int(row["L1"])
        L2 = int(row["L2"])
        L3 = int(row["L3"])
        L4 = int(row["L4"])
        age.connect(L0, L1)
        age.connect(L1, L2)
        age.connect(L2, L3)
        age.connect(L3, L4)

with open("zip.csv", "r") as f:
    for row in csv.DictReader(f):
        L0 = int(row["L0"])
        L1 = int(row["L1"])
        L2 = int(row["L2"])
        L3 = int(row["L3"])
        L4 = int(row["L4"])
        L5 = int(row["L5"])
        zip.connect(L0, L1)
        zip.connect(L1, L2)
        zip.connect(L2, L3)
        zip.connect(L3, L4)
        zip.connect(L4, L5)

D = []
attrs = ["name","surname","age","zip","bank","disease"]

EI = ["name", "surname"] # tokenizzarli
QI = ["age", "zip"]      # generalizzarli o sopprimerli
SD = ["bank", "disease"] # lasciarli invariati

#freq = { qi: {} for qi in QI }

fake = Faker('it_IT')

with open("../data_creation/data.csv", "r") as f:
    for row in csv.DictReader(f):
        D.append(row)

#Creo una tabella di corrispondenza per ogni nome
with open('names.csv', mode='w', newline='') as csv_file:
    fieldnames = ['name', 'fake_name']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    names = set()
    for row in D:
        names.add(row['name'])
    for name in names:
        writer.writerow({'name': name, 'fake_name': fake.unique.first_name()})
#Creo una tabella di corrispondenza per ogni cognome
with open('surnames.csv', mode='w', newline='') as csv_file:
    fieldnames = ['surname', 'fake_surname']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    surnames = set()
    for row in D:
        surnames.add(row['surname'])
    for surname in surnames:
        writer.writerow({'surname': surname, 'fake_surname': fake.unique.last_name()})

# Tokenizzazione su EI
with open("names.csv", "r") as f, open("surnames.csv", "r") as g:
    for attr in EI:
        for row in D:
            if(attr == "name"):
                for row2 in csv.DictReader(f):
                    if(row[attr] == row2['name']):
                        row[attr] = row2['fake_name']
            elif(attr == "surname"):
                for row2 in csv.DictReader(g):
                    if(row[attr] == row2['surname']):
                        row[attr] = row2['fake_surname']
# Generalizzare i QI
"""
gens = []
for attr in QI:
    for row in D:
        val = int(row[attr])
        if val not in freq[attr].keys():
            freq[attr][val] = 0

        freq[attr][val] += 1

    # Generalizzo
    gens.append(pd.cut(list(freq[attr].values()), bins=4, labels=[1,2,3,4]))
"""
anon_level_age = 1
anon_level_zip = 2
with open('../data_creation/AnonData.csv', mode='w', newline='') as csv_file:
    fieldnames = ['name', 'surname', 'age', 'zip', 'bank', 'disease']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for i,attr in enumerate(QI):
        for j,row in enumerate(D):
            val = int(row[attr])
            if(attr == "age"):
                if(anon_level_age == 1):
                    row[attr] = age.generalize(val)
                elif(anon_level_age == 2):
                    row[attr] = age.generalize(age.generalize(val))
                elif(anon_level_age == 3):
                    row[attr] = age.generalize(age.generalize(age.generalize(val)))
                elif(anon_level_age == 4):
                    row[attr] = age.generalize(age.generalize(age.generalize(age.generalize(val))))
            elif(attr == "zip"):
                if(anon_level_zip == 1):
                    row[attr] = zip.generalize(val)
                elif(anon_level_zip == 2):
                    row[attr] = zip.generalize(zip.generalize(val))
                elif(anon_level_zip == 3):
                    row[attr] = zip.generalize(zip.generalize(zip.generalize(val)))
                elif(anon_level_zip == 4):
                    row[attr] = zip.generalize(zip.generalize(zip.generalize(zip.generalize(val))))
                elif(anon_level_zip == 5):
                    row[attr] = zip.generalize(zip.generalize(zip.generalize(zip.generalize(zip.generalize(val)))))

            """
            for _ in range(gens[i][j]):
                if(attr == "age"):
                    D[j][attr] = age.generalize(int(D[j][attr]))
                else:
                    D[j][attr] = zip.generalize(int(D[j][attr]))
                ## genVal = age.generalize(freq[attr][row])
            """
    for x in D : writer.writerow({'name': x['name'], 'surname': x['surname'], 'age': x['age'], 'zip': x['zip'] , 'bank': x['bank'], 'disease': x['disease']})
    print("Data written to anonData.csv")
