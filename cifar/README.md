# CIFAR-10 Dataset Helpers

### Environment:

- Python 3.7.4

### Python Packages:

- numpy
- opencv
- pandas

### Prerequisites:

This project assumes you have the CIFAR-10 Python Dataset directory saved locally on your machine by downloading and extracting the dataset from the [CIFAR Website](https://www.cs.toronto.edu/~kriz/cifar.html) or directly from [this link](https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz). Extracting the tarball from the above link should result in a local directory titled `cifar-10-batches-py`. This directory can be renamed, but do not edit the contents as the dataset generator script assumes the original directory format provided by the dataset website.

### `generate_png_dataset.py`:

Run:

```
$ generate_png_dataset.py <path/to/read/directory> <path/to/write/directory/>
```

This script uses the extracted `cifar-10-batches-py` directory (or whatever you renamed it) to load the CIFAR-10 dataset and re-write it locally as a dataset of PNG files on disk.

The data is organized into training/testing directories of PNG image files accompanied by a `csv` file listing one-to-one correspondences between the image file names and their label. This is summarized by the directory tree structure below.

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
