"""
Generate a dataset of saved PNG images from the MNIST dataset.
"""

import os
import argparse
import mnist
import cv2
import numpy as np

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

    # write labels csvs
    np.savetxt("{}mnist_train_labels.csv".format(args.write_dir), train_labels)
    np.savetxt("{}mnist_test_labels.csv".format(args.write_dir), test_labels)

    # make some new directories at the write location
    if not os.path.exists("{}mnist_train_png".format(args.write_dir)):
        os.mkdir("{}mnist_train_png".format(args.write_dir))
    if not os.path.exists("{}mnist_test_png".format(args.write_dir)):
        os.mkdir("{}mnist_test_png".format(args.write_dir))

    print("[INFO]: writing mnist training images")
    for i, img in enumerate(train_imgs):
        # make filename
        filename = "{}{}{:05d}.png".format(args.write_dir, "mnist_train_png/", i)

        # write image to png
        cv2.imwrite(filename, img)

    print("[INFO]: writing mnist testing images")
    for i, img in enumerate(test_imgs):
        # make filename
        filename = "{}{}{:05d}.png".format(args.write_dir, "mnist_test_png/", i)

        # write image to png
        cv2.imwrite(filename, img)
if __name__=="__main__":
    main()
