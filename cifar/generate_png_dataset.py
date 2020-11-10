"""
Generate a dataset of PNG images from the CIFAR-10 dataset.
Prerequisites: Download and extract the CIFAR-10 for Python dataset here:

https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
"""

import os
import argparse
import pickle
import numpy as np
import pandas as pd
import cv2


def main():
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('read_dir', help='dataset read directory')
    parser.add_argument('write_dir', help='dataset write directory')
    args = parser.parse_args()

    # check confirmation
    if not input(
            '[INFO]: this will write ~125MB of data, proceed? (Y/N): ') == 'Y':
        print('[INFO]: exiting')
        exit()

    # load cifar dataset
    for i in range(1, 6):
        # open the file for this batch of cifar data
        with open(args.read_dir + 'data_batch_' + str(i), 'rb') as fp:
            # if this is the first batch, create a new data array
            if i == 1:
                data_dict = pickle.load(fp, encoding='latin1')
                train_x = np.asarray(data_dict['data'])
                train_y = np.asarray(data_dict['labels'])
                train_x_r = np.reshape(
                    train_x[:, :1024], [train_x.shape[0], 32, 32, 1])
                train_x_g = np.reshape(
                    train_x[:, 1024:2 * 1024], [train_x.shape[0], 32, 32, 1])
                train_x_b = np.reshape(
                    train_x[:, 2 * 1024:], [train_x.shape[0], 32, 32, 1])
                train_x = np.concatenate(
                    [train_x_b, train_x_g, train_x_r], axis=3)
            # if this isn't the first batch, concatenate to existing data array
            else:
                data_dict = pickle.load(fp, encoding='latin1')
                train_x_c = np.asarray(data_dict['data'])
                train_y_c = np.asarray(data_dict['labels'])
                train_x_r = np.reshape(
                    train_x_c[:, :1024], [train_x_c.shape[0], 32, 32, 1])
                train_x_g = np.reshape(
                    train_x_c[:, 1024:2 * 1024],
                    [train_x_c.shape[0], 32, 32, 1])
                train_x_b = np.reshape(
                    train_x_c[:, 2 * 1024:], [train_x_c.shape[0], 32, 32, 1])
                train_x_c = np.concatenate(
                    [train_x_b, train_x_g, train_x_r], axis=3)

                # concatenate the batch to the growing data array
                train_x = np.concatenate([train_x, train_x_c], axis=0)
                train_y = np.concatenate([train_y, train_y_c], axis=0)

        with open(args.read_dir + 'test_batch', 'rb') as fp:
            data_dict = pickle.load(fp, encoding='latin1')
            test_x = np.asarray(data_dict['data'])
            test_y = np.asarray(data_dict['labels'])
            test_x_r = np.reshape(
                test_x[:, :1024], [test_x.shape[0], 32, 32, 1])
            test_x_g = np.reshape(
                test_x[:, 1024:2 * 1024], [test_x.shape[0], 32, 32, 1])
            test_x_b = np.reshape(
                test_x[:, 2 * 1024:], [test_x.shape[0], 32, 32, 1])
            test_x = np.concatenate([test_x_b, test_x_g, test_x_r], axis=3)

    # create labels dataframes
    train_y_df = pd.DataFrame(columns=['Filename', 'Label'])
    test_y_df = pd.DataFrame(columns=['Filename', 'Label'])

    # make some new directories at the write location
    if not os.path.exists('{}train'.format(args.write_dir)):
        os.mkdir('{}train'.format(args.write_dir))
    if not os.path.exists('{}test'.format(args.write_dir)):
        os.mkdir('{}test'.format(args.write_dir))

    print('[INFO]: writing cifar training images')
    for i, img in enumerate(train_x):
        # make filename
        filename = '{}{}{:05d}.png'.format(args.write_dir, 'train/', i)

        # write image to png
        cv2.imwrite(filename, img)

        # append filename and label to labels dataframe
        train_y_df = train_y_df.append(
            {
                'Filename': '{:05d}.png'.format(i),
                'Label': train_y[i],
            },
            ignore_index=True,
        )

    # write train labels to csv
    train_y_df.to_csv('{}train_labels.csv'.format(args.write_dir), index=False)

    print('[INFO]: writing cifar testing images')
    for i, img in enumerate(test_x):
        # make filename
        filename = '{}{}{:05d}.png'.format(args.write_dir, 'test/', i)

        # write image to png
        cv2.imwrite(filename, img)

        # append filename and label to labels dataframe
        test_y_df = test_y_df.append(
            {
                'Filename': '{:05d}.png'.format(i),
                'Label': test_y[i],
            },
            ignore_index=True,
        )

    # write test labels to csv
    test_y_df.to_csv('{}test_labels.csv'.format(args.write_dir), index=False)


if __name__ == '__main__':
    main()
