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

    # chekc confirmation
    if not input('[INFO]: this will write ~125MB of data, proceed? (Y/N): ') \
            == 'Y':
        print('[INFO]: exiting')
        exit()

    # load cifar dataset
    for i in range(1, 6):
        # open the file for this batch of cifar data
        with open(args.read_dir + 'data_batch_' + str(i), 'rb') as fp:
            # if this is the first batch, create a new data array
            if (i == 1):
                data_dict = pickle.load(fp, encoding='latin1')
                X = np.asarray(data_dict['data'])
                Y = np.asarray(data_dict['labels'])
                X_r = np.reshape(X[:, :1024], [X.shape[0], 32, 32, 1])
                X_g = np.reshape(X[:, 1024:2*1024], [X.shape[0], 32, 32, 1])
                X_b = np.reshape(X[:, 2*1024:], [X.shape[0], 32, 32, 1])
                X = np.concatenate([X_b, X_g, X_r], axis=3)
            # if this isnt the first batch, concatenate to existing data array
            else:
                data_dict = pickle.load(fp, encoding='latin1')
                X_c = np.asarray(data_dict['data'])
                Y_c = np.asarray(data_dict['labels'])
                X_r = np.reshape(X_c[:, :1024], [X_c.shape[0], 32, 32, 1])
                X_g = np.reshape(X_c[:, 1024:2*1024], [X_c.shape[0], 32, 32, 1])
                X_b = np.reshape(X_c[:, 2*1024:], [X_c.shape[0], 32, 32, 1])
                X_c = np.concatenate([X_b, X_g, X_r], axis=3)

                # concatenate the batch to the growing data array
                X = np.concatenate([X, X_c], axis=0)
                Y = np.concatenate([Y, Y_c], axis=0)

        with open(args.read_dir + 'test_batch', 'rb') as fp:
            data_dict = pickle.load(fp, encoding='latin1')
            X_test = np.asarray(data_dict['data'])
            Y_test = np.asarray(data_dict['labels'])
            X_r = np.reshape(X_test[:, :1024], [X_test.shape[0], 32, 32, 1])
            X_g = np.reshape(X_test[:, 1024:2*1024], [X_test.shape[0], 32, 32, 1])
            X_b = np.reshape(X_test[:, 2*1024:], [X_test.shape[0], 32, 32, 1])
            X_test = np.concatenate([X_b, X_g, X_r], axis=3)

    num_train = int(0.8 * X.shape[0])
    train_imgs = X[:num_train]
    train_labels = Y[:num_train]
    test_imgs = X[num_train:]
    test_labels = Y[num_train:]

    # create labels dataframes
    train_labels_df = pd.DataFrame(columns=['Filename', 'Label'])
    test_labels_df = pd.DataFrame(columns=['Filename', 'Label'])

    # make some new directories at the write location
    if not os.path.exists('{}train'.format(args.write_dir)):
        os.mkdir('{}train'.format(args.write_dir))
    if not os.path.exists('{}test'.format(args.write_dir)):
        os.mkdir('{}test'.format(args.write_dir))

    print('[INFO]: writing cifar training images')
    for i, img in enumerate(train_imgs):
        # make filename
        filename = '{}{}{:05d}.png'.format(args.write_dir, 'train/', i)

        # write image to png
        cv2.imwrite(filename, img)

        # append filename and label to labels dataframe
        train_labels_df = train_labels_df.append(
            {
                'Filename': '{:05d}.png'.format(i),
                'Label': train_labels[i],
            },
            ignore_index=True,
        )

    # write train labels to csv
    train_labels_df.to_csv('{}train_labels.csv'.format(args.write_dir), index=False)

    print('[INFO]: writing cifar testing images')
    for i, img in enumerate(test_imgs):
        # make filename
        filename = '{}{}{:05d}.png'.format(args.write_dir, 'test/', i)

        # write image to png
        cv2.imwrite(filename, img)

        # append filename and label to labels dataframe
        test_labels_df = test_labels_df.append(
            {
                'Filename': '{:05d}.png'.format(i),
                'Label': test_labels[i],
            },
            ignore_index=True,
        )

    # write test labels to csv
    test_labels_df.to_csv('{}test_labels.csv'.format(args.write_dir), index=False)

if __name__ == '__main__':
    main()
