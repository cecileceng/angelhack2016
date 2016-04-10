import csv

tsv_file = open('responses.tsv','rb')
file_reader = csv.reader(tsv_file,delimiter='\t')

for row in file_reader:
  if row[0] == 'two':
    print row[1]
    break

tsv_file.close()

print '\n'

with open('responses.tsv','rb') as tsvin:
  tsvin = csv.reader(tsvin, delimiter='\t')

  for row in tsvin:
    print row
