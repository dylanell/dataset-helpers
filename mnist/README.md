# MNIST Dataset Helpers

### Environment:

- Python 3.7.4

### Python Packages:

- numpy
- mnist
- opencv
- pandas

### `generate_png_dataset.py`:

Run:

```
$ generate_png_dataset.py <path/to/write/directory/>
```

This script uses the `mnist` Python package to load the MNIST dataset and re-write it locally as a dataset of PNG files on disk.

The MNIST data is organized into training/testing directories of PNG image files accompanied by a `csv` file listing one-to-one correspondences between the image file names and their label. This is summarized by the directory tree structure below.

```
dataset_directory/
|__ train_labels.csv
|__ test_labels.csv
|__ train/
|   |__ train_image_01.png
|   |__ train_image_02.png
|   |__ ...
|__ test/
|   |__ test_image_01.png
|   |__ test_image_02.png
|   |__ ...   
```

Each labels `csv` file has the format:

```
Filename, Label
train_image_01.png, 4
train_image_02.png, 7
...
```
