"""
Add the flip label to the csv files.
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import cv2

# Exceptions
from src.d0_utils.store_load_data.exceptions.exception_classes import FindPathError, AlreadyExistError

# To create a cvs file
from src.d0_utils.store_load_data.fill_csv import create_csv


def get_ways(indexes, changes):
    indexes.append(changes[0])
    print(indexes)
    return np.ones(len(indexes))


def add_swimming_way(video_name, destination_csv, changes):
    """
    Add a column that indicates the swimming way of the swimmers.

    Args:
        video_name (string): the name of the video

        destination_csv (WindowsPath): the path that lead to the csv path.

        changes (list of list of integers): the list of the indexes where swimmers change direction.
    """
    # Get the paths
    csv_path = destination_csv / "{}.csv".format(video_name)
    csv_name_save = "full_{}{}.csv".format(video_name, np.random.randint(1, 10000))
    csv_path_save = destination_csv / csv_name_save

    if not csv_path.exists():
        raise FindPathError(csv_path)

    # Create the new csv
    create_csv(csv_name_save, destination=destination_csv, dictionary={'x_head': [], 'y_head': [], 'swimming_way': []})

    # Load the data
    data_frame = pd.read_csv(csv_path)

    with open(csv_path_save, 'a', newline='') as csv_file:
        # Add the swimming_way column to the data frame
        data_frame["swimming_way"] = get_ways(data_frame.index, changes)

        # Save the changes
        data_frame.to_csv(csv_file, header=False)


if __name__ == "__main__":
    VIDEO_NAME = "vid1"
    DESTINATION_CSV = Path("../data/3_processed_positions/tries")

    CHANGES = [[1, 1000], [1, 1097]]

    try:
        add_swimming_way(VIDEO_NAME, DESTINATION_CSV, CHANGES)
    except FindPathError as find_error:
        print(find_error.__repr__())
    except AlreadyExistError as exist_error:
        print(exist_error.__repr__())
