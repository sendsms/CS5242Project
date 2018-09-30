import os

import progressbar
import numpy as np

# Folders
# Global folder for data
data_folder = os.path.join("..", "training_data")

# Data given (not modified)
original_data_folder = os.path.join(data_folder, "original")

# First extraction of data
extracted_data_folder = os.path.join(data_folder, "extracted")
extracted_data_train_folder = os.path.join(extracted_data_folder, "train")
extracted_data_test_folder = os.path.join(extracted_data_folder, "test")

# Conversion to examples
training_examples_folder = os.path.join(data_folder, "training_examples")

# Suffixes for extracted data files
extracted_protein_suffix = "_pro_cg.csv"
extracted_ligand_suffix = "_lig_cg.csv"

# Some settings for number and persisting tensors
float_type = np.float32
formatter = "%.16f"
comment_delimiter = "#"

# Features used to train:
#  - 3 spatial coordinates : x , y, z (floating values)
#  - 2 features for one hot encoding of atom types (is_hydrophobic, is_polar)
#  - 2 features for one hot encoding of molecules types (is_from_protein, is_from_ligand)

features_names = ["x", "y", "z", "is_hydrophobic", "is_polar", "is_from_protein", "is_from_ligand"]
nb_features = len(features_names)

# We have 3000 positives pairs of ligands
nb_examples = 3000

# We use the split_index first ones to train
split_index = 2700
# All the other will be used to construct examples on the go

# We augment the number of examples
nb_neg_ex_per_pos = 10

# To scale protein-ligands system in a cube of shape (resolution_cube,resolution_cube,resolution_cube)
resolution_cube = 30

# Obtained with values_range on the complete original dataset
hydrophobic_types = {"C"}
polar_types = {'P', 'O', 'TE', 'F', 'N', 'AS', 'O1-', 'MO',
               'B', 'BR', 'SB', 'RU', 'SE', 'HG', 'CL',
               'S', 'FE', 'ZN', 'CU', 'SI', 'V', 'I', 'N+1',
               'N1+', 'CO', 'W', }

x_min = -244.401
x_max = 310.935

y_min = -186.407
y_max = 432.956

z_mix = -177.028
z_max = 432.956
##

# Misc.
widgets_progressbar = [
    ' [', progressbar.Timer(), '] ',
    progressbar.Bar("░", fill="⋅"),
    ' (', progressbar.ETA(), ') ',
]


def progress(iterable):
    """
    Custom progress bar
    :param iterable:
    :return:
    """
    return progressbar.progressbar(iterable, widgets=widgets_progressbar, redirect_stdout=True)


def extract_id(file_name):
    new_name = file_name.replace(extracted_protein_suffix, "").replace(extracted_ligand_suffix, "")
    return new_name
