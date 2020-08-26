"""
Generate a dataset of saved PNG images from the MNIST dataset.
"""

# TODO: directly append to csv labels file to speed this up

import os
import argparse
import mnist
import cv2
import pandas as pd

def main():
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("write_dir", help="dataset write directory")
    args = parser.parse_args()

    # ask for confirmation
    if not input("[INFO]: this will write ~40MB of data, proceed? (Y/N): ") == 'Y':
        print("[INFO]: exiting")
        exit()

    # load mnist dataset
    train_imgs = mnist.train_images()
    test_imgs = mnist.test_images()
    train_labels = mnist.train_labels()
    test_labels = mnist.test_labels()

    # create labels dataframes
    train_labels_df = pd.DataFrame(columns=['Filename', 'Label'])
    test_labels_df = pd.DataFrame(columns=['Filename', 'Label'])

    # make some new directories at the write location
    if not os.path.exists("{}train".format(args.write_dir)):
        os.mkdir("{}train".format(args.write_dir))
    if not os.path.exists("{}test".format(args.write_dir)):
        os.mkdir("{}test".format(args.write_dir))

    print("[INFO]: writing mnist training images")
    for i, img in enumerate(train_imgs):
        # make filename
        filename = "{}{}{:05d}.png".format(args.write_dir, "train/", i)

        # write image to png
        cv2.imwrite(filename, img)

        # append filename and label to labels dataframe
        train_labels_df = train_labels_df.append(
            {
                'Filename': "{:05d}.png".format(i),
                'Label': train_labels[i],
            },
            ignore_index=True,
        )

    # write train labels to csv
    train_labels_df.to_csv("{}train_labels.csv".format(args.write_dir), index=False)

    print("[INFO]: writing mnist testing images")
    for i, img in enumerate(test_imgs):
        # make filename
        filename = "{}{}{:05d}.png".format(args.write_dir, "test/", i)

        # write image to png
        cv2.imwrite(filename, img)

        # append filename and label to labels dataframe
        test_labels_df = test_labels_df.append(
            {
                'Filename': "{:05d}.png".format(i),
                'Label': test_labels[i],
            },
            ignore_index=True,
        )

    # write test labels to csv
    test_labels_df.to_csv("{}test_labels.csv".format(args.write_dir), index=False)

if __name__=="__main__":
    main()
