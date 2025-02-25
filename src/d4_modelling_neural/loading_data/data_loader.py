"""
This module loads the image one by one when the object is called. It can perform data augment.
"""
from pathlib import Path
import random as rd
import numpy as np
import cv2

# Exceptions
from src.d4_modelling_neural.loading_data.transformations.tools.exceptions.exception_classes import FindPathDataError, PaddingError, SwimmingWayError

# To generate the data
from src.d4_modelling_neural.loading_data.data_generator import generate_data

# Higher Modules
from tensorflow.keras.utils import Sequence
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# To transform the image
from src.d4_modelling_neural.loading_data.transformations.image_transformations import transform_image


class DataLoader(Sequence):
    """
    The class to load the data.
    """
    def __init__(self, data, batch_size=2, scale=35, dimensions=[108, 1820], standardization=True, augmentation=False, flip=True):
        """
        Create the loader.

        Args:
            data (list of 4 : [WindowsPath, integer, integer, integer, float):
                List of [image_path, x_head, y_head, swimming_way, video_length]
                if swimming_way = 1, the swimmer swims toward the right.
                if swimming_way = -1, the swimmer swims toward the left.

            batch_size (integer): the size of the batches
                Default value = 2

            scale (integer): the number of pixel per meters.
                Default value = 35

            dimensions (list of 2 integers): the final dimensions of the image. [vertical, horizontal]
                Default value = [110, 1820]

            standardization (boolean): standardize the lane_magnifier if standardization = True.
                Default value = True

            augmentation (boolean): if True, data_augmenting is performed.
                Default value = False

            flip (boolean): if True, each image where the swimmer is swimming toward the left side is flipped.
                Default value = True
        """
        # The data
        self.samples = data[:, 0]
        self.labels = data[:, 1: -1]
        self.video_length = data[:, -1]

        # The parameters
        self.batch_size = batch_size
        self.scale = scale
        self.dimensions = dimensions
        self.standardization = standardization
        self.augmentation = augmentation
        self.flip = flip

    def __len__(self):
        """
        Returns the length of the object, i.e. the number of batches.
        """
        return int(np.ceil(len(self.samples) / self.batch_size))

    def __getitem__(self, idx):
        """
        Load the item at the index idx, i.e. a batch.

        Args:
            idx (integer): the wanted index.

        Returns:
            (array, 4 dimensions): list of images.

            (array, 3 dimensions): list of the labels linked to the images.
        """
        # Get the paths, the LABELS and the lengths of the videos
        batch_path = self.samples[idx * self.batch_size: (idx + 1) * self.batch_size]
        batch_labels = self.labels[idx * self.batch_size: (idx + 1) * self.batch_size].astype(float)
        batch_video_length = self.video_length[idx * self.batch_size: (idx + 1) * self.batch_size]

        # Get the specific size of the batch
        length_batch = len(batch_path)

        batch_img = []
        batch_labs = []

        for idx_img in range(length_batch):
            # Get the information
            image_path = batch_path[idx_img]
            label = batch_labels[idx_img]
            video_length = batch_video_length[idx_img]

            # Get the image and transform it
            (trans_image, trans_label) = transform_image(image_path, label, self.scale, video_length, self.dimensions, self.standardization, self.augmentation, self.flip)

            # Fill the lists
            batch_img.append(trans_image)
            batch_labs.append(trans_label)

        return np.array(batch_img, dtype=np.float32), np.array(batch_labs, dtype=np.float32)

    def on_epoch_end(self):
        """
        Shuffle the data set.
        """
        full_data = list(zip(self.samples, self.labels, self.video_length))
        rd.shuffle(full_data)
        (self.samples, self.labels, self.video_length) = zip(*full_data)
        self.samples = np.array(self.samples)
        self.labels = np.array(self.labels)
        self.video_length = np.array(self.video_length)


if __name__ == "__main__":
    PATHS_LABEL = [Path("../../../data/3_processed_positions/tries/vid0.csv"),
                   Path("../../../data/3_processed_positions/tries/vid1.csv")]

    try:
        TRAIN_DATA = generate_data(PATHS_LABEL, take_all=False)

        TRAIN_SET = DataLoader(TRAIN_DATA, scale=35, batch_size=1, standardization=False, augmentation=True, flip=True)

        # Test on_epoch_end()
        TRAIN_SET.on_epoch_end()

        for (IDX, (BATCH, LABELS)) in enumerate(TRAIN_SET):
            # Print the name of the image
            print(TRAIN_SET.samples[IDX])
            print(TRAIN_SET.labels[IDX])
            print(TRAIN_SET.video_length[IDX])

            # Get the image
            image = BATCH[0]

            # Show the label in the image
            image[int(LABELS[0][0]), int(LABELS[0][1])] = [0, 0, 255]

            # Get the correct type to plot
            image = image.astype(np.uint8)

            # Plot the image
            cv2.imshow("Image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    except FindPathDataError as find_path_data_error:
        print(find_path_data_error.__repr__())
    except PaddingError as padding_error:
        print(padding_error.__repr__())
    except SwimmingWayError as swimming_way_error:
        print(swimming_way_error.__repr__())
