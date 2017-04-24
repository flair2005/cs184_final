import os

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from plyfile import PlyData, PlyElement


def get_vertices(plydata):
    return np.hstack(
        [plydata.elements[0].data['x'].reshape(-1, 1),
         plydata.elements[0].data['y'].reshape(-1, 1),
         plydata.elements[0].data['z'].reshape(-1, 1)],
    )


def get_faces(plydata):
    return np.vstack([x[0] for x in plydata.elements[1].data])


def get_vertex_normals(plydata, vertices=None):
    if vertices is None:
        vertices = get_vertices(plydata)

    vertex_normals = np.zeros_like(vertices)
    faces = get_faces(plydata)

    A = vertices[faces[:, 0], :]
    B = vertices[faces[:, 1], :]
    C = vertices[faces[:, 2], :]

    normals = np.cross(A - B, A - C)
    normals = normals / np.linalg.norm(normals, axis=1, keepdims=True)

    vertex_normals[faces[:, 0], :] += normals
    vertex_normals[faces[:, 1], :] += normals
    vertex_normals[faces[:, 2], :] += normals

    return vertex_normals / np.linalg.norm(vertex_normals, axis=1, keepdims=True)



if __name__ == '__main__':

    # point_arrays = []
    # for name in os.listdir('data/bunny/data'):
    #     if name.endswith('.ply'):
    #         plydata = PlyData.read(os.path.join('data/bunny/data', name))
    #         import pdb; pdb.set_trace()
    #         point_arrays.append(
    #             get_vertices(plydata)
    #         )
    #
    # total_data = np.vstack(point_arrays)
    plydata = PlyData.read('data/bunny.ply')
    normals = get_vertex_normals(plydata)
    # import pdb; pdb.set_trace()
    total_data = get_vertices(plydata)

    sample_indices = np.random.randint(0, total_data.shape[0], 1000)

    point_matrix_sampled = total_data[
        sample_indices,
        :
    ]

    increased = 0.01 * normals[
        sample_indices,
        :
    ] + point_matrix_sampled

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(
        point_matrix_sampled[:, 0],
        point_matrix_sampled[:, 2],
        point_matrix_sampled[:, 1],
        c='red'
    )

    ax.scatter(
        increased[:, 0],
        increased[:, 2],
        increased[:, 1],
        c='blue'
    )

    plt.show()
