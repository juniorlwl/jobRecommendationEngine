# NLP

## Dependencies

Either start using pipenv and run `pipenv install` or install the following dependencies manually before running the code:

- spacy
- pypdf2

## Data

### Get RAW Jobs from AWS Athena

The job descriptions were fetched from Athena using the following query:

```sql
SELECT CAST(job_description AS JSON) FROM jobs WHERE location_country = 'US'
AND (lower(job_description) LIKE '%bachelor%degree%'
OR lower(job_description) LIKE '% bsc%degree%'
OR lower(job_description) LIKE '% master%degree%'
OR lower(job_description) LIKE '% msc%degree%'
OR lower(job_description) LIKE '% mas%degree%'
OR lower(job_description) LIKE '% ms%degree%'
OR lower(job_description) LIKE '% bs%degree%' ) GROUP BY job_description ORDER BY RANDOM() LIMIT 5000
```

This query ensures that we got descriptions requiring higher eductation, which are usually of higher quality as well.

### Conver RAW Jobs to JSONL

```
python convert.py raw datasets/jobs.csv job_data.jsonl
```

### Convert Job Descriptions to Prodigy Compatible JSONL

```
python convert.py csv datasets/job_descriptions.csv jobs.jsonl
```

### Convert PDF Resumes to Prodigy Compatible JSONL

```
python convert.py pdf resumes/ resumes.jsonl
```

or a single resume

```
python convert.py pdf resumes/resume.pdf resumes.jsonl
```

Use the `--extend` flag to append to a file and extend an existing dataset.

```
python convert.py pdf resumes/resume.pdf resumes.jsonl --extend
```

### Reduce Prodigy Annotations to one Label

```
python convert.py label datasets/full_annotation.jsonl datasets/reduced_annotation -l SKILL
```

## Prodigy

When working with prodigy, it is important to make regular backups of the dataset:
```
prodigy db-out resumes .
```

Also check out the all the available recipes in the documentation. There are a lot of helpful commands: https://prodi.gy/docs/recipes

### Create a new Gold Dataset of Annotations

This is the initial creation of a set of manual annotations.

```
prodigy ner.make-gold resumes ./blank-model data.jsonl -U --label "DEGREE, SKILL, EXPERIENCE"
```

### Train the Model Using the Annotations

This command uses the annotations in the database.

```
prodigy ner.batch-train resumes ./blank-model --output ./trained-model --n-iter 10
```

### Teach an Existing Model

This command allows us to teach the model further using binary answers. This can be done once we have reasonable results with the gold annotations.

```
prodigy ner.teach resumes ./trained-model ./data.jsonl
```

### Inspect the Results
This will highlight the annotations made by the model in the command line.
```
prodigy ner.print-stream ./trained-model jobs.jsonl
```

## Spacy

### Create a Blank Model

```
python blank_model.py ./models/blank_model
```

### Train the model

The `train.py` script takes a file containing exported annotations from Doccano, trains a model on it and stores the resultig model in the given directory.

```
python train.py --input-file=./annotated_jobs.csv --output-dir=./model
```

### Annotate new Data

To annotate new data using a trained model, use `annotate.py`. The input needs to be a csv containing one text per line.

```
python annotate.py --input-file=./texts.csv --model-dir=./model --output-file=./annotated.json
```

### Visualize Annotations

To visualize text previously annotated by `annotate.py`, you can use `visualize.py`. Taking only the input file as an argument. This starts a webserver which displays your results.

```
python visualize.py --input-file=./annotated.json
```
