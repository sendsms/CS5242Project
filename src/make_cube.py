import numpy as np
import os
import matplotlib.pyplot as plt


from mpl_toolkits.mplot3d import Axes3D # needed by the 3D plotter
from settings import float_type, comment_delimiter, examples_data, resolution_cube


def cuboise(example: np.ndarray, res):
    # For now making cubes really naively as follow:
    # Scaling on each coordinates : the result can be distorted.
    # Rounding down each time (not to the closest

    coords = example[:, 0:3]
    atom_features = example[:, 3:]
    nb_features = atom_features.shape[1]

    # Getting extreme values
    x_min, x_max, y_min, y_max, z_min, z_max = values_range(coords)

    # Scaling coordinates to be in the cube [0,res]^3 then flooring
    scaled_coords = (coords * 0).astype(int)
    eps = 10e-4  # To be sure to round down on exact position
    scaled_coords[:, 0] = np.floor((coords[:, 0] - x_min) / (x_max - x_min + eps) * res).astype(int)
    scaled_coords[:, 1] = np.floor((coords[:, 1] - y_min) / (y_max - y_min + eps) * res).astype(int)
    scaled_coords[:, 2] = np.floor((coords[:, 2] - z_min) / (z_max - z_min + eps) * res).astype(int)

    cube = np.zeros((res, res, res, nb_features))

    # Filling the cube with the features
    cube[scaled_coords[:, 0], scaled_coords[:, 1], scaled_coords[:, 2]] = atom_features

    return cube


def only_positive_examples(examples):
    def is_positive(name):
        systems = name.replace(".csv", "").split("_")
        return systems[0] == systems[1]

    return list(filter(is_positive, examples))


def values_range(spatial_coordinates):
    x_min = np.min(spatial_coordinates[:, 0])
    y_min = np.min(spatial_coordinates[:, 1])
    z_min = np.min(spatial_coordinates[:, 2])

    x_max = np.max(spatial_coordinates[:, 0])
    y_max = np.max(spatial_coordinates[:, 1])
    z_max = np.max(spatial_coordinates[:, 2])

    return x_min, x_max, y_min, y_max, z_min, z_max


def plot_cube(cube):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    xs = []
    ys = []
    zs = []
    cs = []
    for x in range(resolution_cube):
        for y in range(resolution_cube):
            for z in range(resolution_cube):
                c = cube[x, y, z, 1] # plotting accordingly to the molecule
                print()
                if c != 0:
                    xs.append(x)
                    ys.append(y)
                    zs.append(z)
                    cs.append(c)

    ax.scatter(xs, ys, zs, c=cs, marker="o")

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()


if __name__ == "__main__":

    examples = sorted(os.listdir(examples_data))
    positives = only_positive_examples(examples)
    for example in positives:
        file_name = os.path.join(examples_data, example)

        example = np.loadtxt(file_name, dtype=float_type, comments=comment_delimiter)
        cube = cuboise(example, resolution_cube)
        print(cube.shape)
        plot_cube(cube)
        break