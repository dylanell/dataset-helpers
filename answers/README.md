# Answers.com Topic Dataset Helpers

This project scrapes question-answer pairs from a specific topic on [Answers.com](https://www.answers.com/).

### Environment:

- Python 3.7.4

### Python Packages:

- pandas
- bs4

### Prerequisites:

Before running `generate_dataset.py` to scrape data on a specific topic, you should check that the topic category exists in Answers.com by verifying that there is a *topic tile* for that topic. The URL passed to `generate_dataset.py` should be the landing page URL for the specific topic (from selecting a topic tile). For example, to check that a topic category for "Diabetes" exists, you could first start by searching a question about diabetes, such as "What is diabetes?". Selecting the first answer should bring you to [this answer page](https://www.answers.com/Q/What_is_Diabetes), which will have topic tiles along the top of the question block. In this case, a topic tile for "Diabetes" should be present. Clicking this tile will then bring you to the first Answers.com page for the topic of "Diabetes", which should now be at the url: "https://www.answers.com/t/diabetes". Since this URL corresponds to an existing topic in Answers.com, can pass it to the `generate_dataset.py` script in this project to scrape the data from multiple pages on this topic.

### `generate_dataset.py`:

Run:

```
$ generate_png_dataset.py https://www.answers.com/t/<your_topic> <path/to/write/directory/>
```

Optionally, change the `min_samples` argument to control the minimum number of samples to scrape. The script writes question-answer pairs to a `qa_pairs.csv` file after collecting at least `min_samples` question-answer pairs, or by running out of topic pages.

The `qa_pairs.csv` file has the format:

```
Question, Answer
Query 1 text?, Response 1 text.
Query 2 text?, Response 2 text.
...
```