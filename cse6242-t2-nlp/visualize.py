import plac
import json
from spacy import displacy


@plac.annotations(
    input_file=("JSON input file", "option", "i", str))
def main(input_file):
    with open(input_file, "r") as json_file:
        data = json.loads(json_file.read())

        annotations = []

        for document in data:
            annotations.append({'text': document[0],
                                'ents': [{'start': entity[0], 'end': entity[1], 'label': entity[2]} for entity in document[1]['entities']],
                                'title': None})

        displacy.serve(annotations, style='ent', options={'colors': {
                       'EXPERIENCE': 'rgb(255, 0, 128)', 'SKILL': 'rgb(32, 156, 238)', 'DEGREE': 'rgb(0, 179, 0)'}}, manual=True)


if __name__ == '__main__':
    plac.call(main)
