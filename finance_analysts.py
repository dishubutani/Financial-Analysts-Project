import csv
file = open('European_Bank.csv', mode='r', newline='', encoding='latin-1', errors='ignore')
reader = csv.reader(file)
    for row in reader:
        print(row)
encoding='cp1252'
