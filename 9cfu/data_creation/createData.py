from faker import Faker
from random import randint
import csv

fake = Faker('it_IT')

# Open the CSV file in write mode
with open('data.csv', mode='w', newline='') as csv_file:
    fieldnames = ['name', 'surname', 'age', 'zip', 'bank', 'disease']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    possible_disease = ["influenza", "polmonite", "broncopolmonite", "influenza Intestinale", "mononucleosi", "covid-19"] 

    # Write the header
    writer.writeheader()

    # Generate and write 10 rows of fake data
    for _ in range(1000):
        name = fake.first_name()
        surname = fake.last_name()
        age = randint(1, 99)
        zip_code = randint(16000, 16999)
        
        if(age < 18):
            credit_card_number =  randint(0,10000)
        elif(age > 18 and age < 35):
            credit_card_number =  randint(5000,50000)
        else:
            credit_card_number =  randint(1000,100000)
        disease = possible_disease[randint(0, len(possible_disease) - 1)]

        # Write the data to the CSV file
        writer.writerow({'name': name, 'surname': surname, 'age': age, 'zip': zip_code, 'bank': credit_card_number, 'disease': disease})

print("Data written to data.csv")