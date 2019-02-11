import re
import csv

def to_spacy(filename):
    CSVFILENAME = str(filename)

    #Get RowCount of the CSV File
    with open(str(CSVFILENAME), encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_count = sum(1 for row in csv_reader)

    #CSV Processing
    with open(str(CSVFILENAME), encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        current_annotation = None
        current_document = None
        current_description = ''
        current_start = None
        row_number = 0
        current_entities = []
        data = []

        for row in csv_reader:
            if row_number == 0:
                current_document = row[0]

            if row[2][0] == 'B':
                # B indicates a new annotation
                current_start = len(current_description)
                current_annotation = row[2]

            if current_annotation != None and (row[2][0] == 'O' or row_count == row_number):
                # If we have reached the last row or the end of the current annotation we write
                # it into the entities list
                end = len(current_description)

                if row[2][0] != 'O':
                    end += 1

                current_entities.append((current_start, end, re.sub(r"^[A-Z]-", "", current_annotation)))
                current_annotation = None

            row_number += 1

            if row[0] != current_document or row_count == row_number:
                # If we start with a new document or reach the end of the file we
                #  write the document into the final result list
                data.append((current_description, {
                   "entities": current_entities
                }))

                current_entities = []
                current_document = row[0]
                current_description = row[1]
            else:
                current_description += row[1]

        return data
