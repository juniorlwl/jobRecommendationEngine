prodigy terms.teach resumes ./blank-model --seeds "Bachelor, Master, BSC, MSC, MS, PhD"

prodigy ner.teach resumes ./blank-model ./data.jsonl --label "DEGREE"


prodigy ner.teach resumes ./blank-model ./data.jsonl --patterns ../spacy/patterns.jsonl

prodigy ner.teach resumes ./blank-model ./data.jsonl --patterns ../spacy/patterns.jsonl

prodigy ner.batch-train resumes ./blank-model --output ./new-model --n-iter 10



prodigy ner.make-gold resumes ./blank-model data.jsonl --patterns patterns-2.jsonl



prodigy net.manual resumes ./data.jsonl --label DEGREE

## Important

Always create a backup of the dataset when doing another iteration of teaching.
```
prodigy db-out resumes /tmp
```
## Create blank model

```python
nlp = spacy.blank('en')
nlp.add_pipe(nlp.create_pipe('ner'))  # add blank NER component
nlp.add_pipe(nlp.create_pipe('sentencizer')) # add sentence boundary detector, just in case
nlp.begin_training()  # initialize weights
nlp.to_disk('./blank-model')  # save out model
```

### Create a new Annotations

```
prodigy ner.make-gold resumes ./blank-model data.jsonl -U --label "DEGREE, SKILL, EXPERIENCE"
```

You can also use a `patterns.jsonl` file in order to kickstart the annotation process. This will probably make sense for EXPERIENCE and DEGREE but not so much for SKILL.

### Train the model using the annotations

```
prodigy ner.batch-train resumes ./blank-model --output ./trained-model --n-iter 10
```

### Do further Teaching

```
prodigy ner.teach resumes-v1 ./trained-model ./data.jsonl
```

Teaching a
prodigy ner.teach resumes-v1 ./trained-model ./data.jsonl --label DEGREE



Todo:
- https://spacy.io/api/lemmatizer
- write script to convert job desc to jsonl
- Add trained model to github of job desc
- Create sample output for job description
- ner.gold-to-spacy
