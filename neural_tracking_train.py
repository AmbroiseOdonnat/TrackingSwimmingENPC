"""
This script allows the user to train some MODEL.
"""
# Exceptions
from src.d4_modelling_neural.loading_data.transformations.tools.exceptions.exception_classes import FindPathDataError, PaddingError
from src.d0_utils.store_load_data.exceptions.exception_classes import AlreadyExistError

# To train the MODEL
from src.d4_modelling_neural_magnifier import train_magnifier

# The main module
import tensorflow as tf


# --- BEGIN : !! TO MODIFY !! --- #
REAL_TRAINING = True
# Parameters for data
VIDEO_NAMES_TRAIN = ["vid0"]
VIDEO_NAMES_VALID = ["vid1"]
NUMBER_TRAINING = 2
DIMENSIONS = [108, 1820]

# Parameters for loading the data
SCALE = 35
AUGMENTATION = True

# Parameters for the training
NB_EPOCHS = 15
BATCH_SIZE = 12
WINDOW_SIZE = 150
NB_SAMPLES = 3
DISTRIBUTION = 0.3
MARGIN = 10
TRADE_OFF = 0
# --- END : !! TO MODIFY !! --- #


# Pack the variables
DATA_PARAM = [VIDEO_NAMES_TRAIN, VIDEO_NAMES_VALID, NUMBER_TRAINING, DIMENSIONS]
LOADING_PARAM = [SCALE, AUGMENTATION]
TRAINING_PARAM = [NB_EPOCHS, BATCH_SIZE, WINDOW_SIZE, NB_SAMPLES, DISTRIBUTION, MARGIN, TRADE_OFF]


"""# To avoid memory problems
TF_CONFIG_ = tf.compat.v1.ConfigProto()
TF_CONFIG_.gpu_options.allow_growth = True
sess = tf.compat.v1.Session(config=TF_CONFIG_)"""

# Set the parameter TRIES #
if REAL_TRAINING:
    TRIES = ""
else:
    TRIES = "/tries"

# -- Verify that a GPU is used -- #
print("Is a GPU used for computations ?\n", tf.config.experimental.list_physical_devices('GPU'))

try:
    train_magnifier(DATA_PARAM, LOADING_PARAM, TRAINING_PARAM, TRIES)
except AlreadyExistError as exist_error:
    print(exist_error.__repr__())
except FindPathDataError as find_path_data_error:
    print(find_path_data_error.__repr__())
except PaddingError as padding_error:
    print(padding_error.__repr__())
