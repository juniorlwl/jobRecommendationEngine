import plac
import spacy

@plac.annotations(
    output_dir=plac.Annotation("Connection string", type=str))
def main(output_dir):
    nlp = spacy.blank('en')
    nlp.add_pipe(nlp.create_pipe('ner'))
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    nlp.begin_training()
    nlp.to_disk(output_dir)

if __name__ == '__main__':
    plac.call(main)
