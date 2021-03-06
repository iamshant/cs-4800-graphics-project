#!/usr/bin/python
import argparse
from os import listdir, makedirs
from os.path import exists, join, splitext
from shutil import copy
from random import random


def ensure_directory(dir_path):
    if not exists(dir_path):
        makedirs(dir_path)


def make_dataset_dir(path):
    ensure_directory(path)

    img_dir = join(path, 'images')
    if not exists(img_dir):
        makedirs(img_dir)

    ann_dir = join(path, 'annotations')
    if not exists(ann_dir):
        makedirs(ann_dir)


def get_files_by_ext(dir_path, file_ext):
    return [f for f in listdir(dir_path) if splitext(f)[1] == file_ext]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("src", help="The full path to the source data directory containing the images and annotations.",
                        type=str)
    parser.add_argument("dest", help="The full path to the destination directory for the data set.",
                        type=str)
    parser.add_argument("-tp", "--train-percent", help="The decimal value representing the percentage of samples "
                        "to add to the training set (the rest are added to the validation set).",
                        type=float, action="store", default=0.8, dest="tp")
    parser.add_argument("-ix", "--img-ext", help="The file extension of sample images.",
                        type=str, action="store", default=".jpg", dest="ix")
    parser.add_argument("-ax", "--ann-ext", help="The file extension of image annotations.",
                        type=str, action="store", default=".xml", dest="ax")
    parser.add_argument("-id", "--img-src", help="The image directory within the src directory.",
                        type=str, action="store", default="images", dest="id")
    parser.add_argument("-ad", "--ann-src", help="The annotation directory within the src directory.",
                        type=str, action="store", default="annotations", dest="ad")
    args = parser.parse_args()

    src_dir_path = args.src
    dest_dir_path = args.dest

    percent_train = args.tp  # default = 0.8

    img_file_ext = args.ix  # default = '.jpg'
    ann_file_ext = args.ax  # default = '.xml'

    img_src_dir = join(src_dir_path, args.id)
    ann_src_dir = join(src_dir_path, args.ad)
    train_dir = join(dest_dir_path, 'train')
    validation_dir = join(dest_dir_path, 'validation')

    make_dataset_dir(train_dir)
    make_dataset_dir(validation_dir)

    def save_to_train(img_file, ann_file):
        copy(img_file, join(train_dir, 'images'))
        copy(ann_file, join(train_dir, 'annotations'))

    def save_to_validation(img_file, ann_file):
        copy(img_file, join(validation_dir, 'images'))
        copy(ann_file, join(validation_dir, 'annotations'))


    samples = get_files_by_ext(img_src_dir, img_file_ext)

    for sample in samples:
        sample_ann = splitext(sample)[0] + ann_file_ext

        img_file = join(img_src_dir, sample)
        ann_file = join(ann_src_dir, sample_ann)

        if not exists(ann_file):
            continue

        if random() < percent_train:
            save_to_train(img_file, ann_file)
        else:
            save_to_validation(img_file, ann_file)




