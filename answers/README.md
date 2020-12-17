# Answers.com Topic Dataset Helpers

This project scrapes question-answer pairs from a specific topic on [Answers
.com](https://www.answers.com/).

### Environment:

- Python 3.8.5

### Install Python Packages:

```
$ pip install -r requirements.txt
```

### Prerequisites:

Before running `generate_dataset.py` to scrape data on a specific topic, you
should check that the topic category exists in "Answers.com" by verifying
that there is a *topic tile* for that topic. The URL passed to
`generate_dataset.py` should be the landing page URL for the specific topic
(from selecting a topic tile). For example, to check that a topic category
for "Diabetes" exists, you could first start by searching a question about
diabetes, such as "What is diabetes?". Selecting the first answer should
bring you to [this answer page](https://www.answers.com/Q/What_is_Diabetes
), which will have topic tiles along the top of the question block. In this
case, a topic tile for "Diabetes" should be present. Clicking this tile will
then bring you to the first "Answers.com" page for the topic of "Diabetes
", which should now be at the url: "https://www.answers.com/t/diabetes
". Since this URL corresponds to an existing topic in Answers.com, can pass
it to the `generate_dataset.py` script in this project to scrape the data
from multiple pages on this topic.

### `generate_dataset.py`:

Run:

```
$ python generate_png_dataset.py https://www.answers.com/t/<your_topic> <path/to/write/directory/>
```

Optionally, change the `min_samples` argument to control the minimum number
 of samples to scrape. The script writes pre-processed question-answer pairs
  to a `pickle` file after collecting at least `min_samples` question-answer
   pairs, or by running out of topic pages.

Running the above script produces two artifacts; a data file of question
-answer pairs accompanied by a vocabulary dictionary mapping unique integer
 values to every unique word found in the question-answer pairs data file.

The question-answer pairs data file is saved in both unprocessed and
 processed formats. The unprocessed data file is witten in the format:

```
Question Raw, Answer Raw,
Raw question 1, Raw answer 1
Raw question 2, Raw answer 2
...
```

The processed data file is written in the format:

```
Question Processed, Answer Processed,
Processed question 1, Processed answer 1
Processed question 2, Processed answer 2
...
```

The processed data file is constructed such that simple tokenization by
 whitespace can be performed if using this data file for NLP applications.

### References:

1. General text normalization and processing:
  - https://medium.com/@datamonsters/text-preprocessing-in-python-steps-tools-and-examples-bf025f872908

2. Text decontraction:
  - https://stackoverflow.com/q/49007346

3. Flattening lists of lists while ignoring strings:
  - https://stackoverflow.com/a/17867797
