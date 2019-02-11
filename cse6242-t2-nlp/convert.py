import PyPDF2
import os
import json
import plac
from pathlib import Path
import codecs
from io import StringIO
import string
import csv
from modules import cleaner


@plac.annotations(
    command=plac.Annotation("command", type=str),
    input_source=plac.Annotation("Connection string", type=Path),
    output_file=plac.Annotation("Connection string", type=Path),
    label=plac.Annotation("Label",  'option', 'l', type=str),
    extend=plac.Annotation("Extend an exsiting dataset", 'flag', 'e'))
def main(command, input_source, output_file, label, extend):
    output_mode = 'a' if extend else 'w'

    if command == 'pdf':
        # Convert the pdfs of the given directory or if the input is a single file only this file

        with open(str(output_file), output_mode) as jsonl_file:

            if str(input_source).endswith(".pdf"):
                text = pdf_to_text(str(input_source))

                jsonl_file.write(json.dumps({"text": text.strip('\n')}) + '\n')
            else:
                for filename in os.listdir(str(input_source)):
                    if not filename.endswith(".pdf"):
                        continue

                    text = pdf_to_text(os.path.join(
                        str(input_source), filename))

                    jsonl_file.write(json.dumps(
                        {"text": text.strip('\n')}) + '\n')

    elif command == 'csv':
        # Convert all the texts in the csv

        with open(str(output_file), output_mode) as jsonl_file:
            with open(str(input_source), encoding="utf8") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                next(csv_reader)  # Skip header row.

                for row in csv_reader:
                    text = preprocess_text(json.loads(row[0]))
                    jsonl_file.write(json.dumps(
                        {"text": text.strip('\n')}) + '\n')
    elif command == 'raw':
        # Convert the raw data to jsonl

        with open(str(output_file), output_mode) as jsonl_file:
            with open(str(input_source), encoding="utf8") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                headers = next(csv_reader, None)

                for row in csv_reader:
                    data =  dict(zip(headers, [decode_if_json(cell) for cell in row]))

                    jsonl_file.write(json.dumps(data) + '\n')
    elif command == 'label':
        # Convert the raw data to jsonl

        with open(str(output_file), output_mode) as jsonl_file:
            with open(str(input_source), encoding="utf8") as f:
                lines = f.readlines()

                for line in lines:
                    line = line.rstrip('\n')
                    annotation = json.loads(line)

                    if 'spans' not in annotation.keys():
                        continue

                    annotation['spans'] = [span for span in annotation['spans'] if span['label'] == label]

                    jsonl_file.write(json.dumps(annotation) + '\n')

def decode_if_json(s):
    try:
        return json.loads(s)
    except ValueError:
        return s

def preprocess_text(text):
    # Strip all HTML tags
    text = cleaner.strip_tags(text)

    # Drop all non-ascii characters
    #text = ''.join(filter(lambda x: x in set(string.printable), text))
    text = ''.join([i if ord(i) < 128 else ' ' for i in text])
    return text


def pdf_to_text(filepath):
    text = ''

    pdfFileObj = open(filepath, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    for page in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(page)
        text += pageObj.extractText()

    return preprocess_text(text)


if __name__ == '__main__':
    plac.call(main)
