import numpy as np
import cv2
import matplotlib.pyplot as plt
import open3d as o3d
import os

class Camera:
    """
    Camera class for simulating each camera in a stereoscopic setup.
    """
    def __init__(self, width, height, f, coordinate: list, orientation: list):
        self.width = width              # width of the camera sensor in mm
        self.height = height            # height of the camera sensor in mm
        self.f = f                      # focal length of the camera lens
        self.coordinate = coordinate    # coordinate position of the camera [x, y, z]
        self.orientation = orientation  # orientation of the camera [Rx,Ry,Rz] in degrees

    def capture(self):
        "will capture an image of the scene"
        self.img = np.zeros([self.width, self.height])  # creating blank image placeholder
        pass


class Object:
    def __init__(self,filename: str, position: list, orientation: list):
        if not isinstance(filename, str):
            raise TypeError("The filename must be a string.")

        self.mesh = o3d.io.read_triangle_mesh(filename)

        # Check if the mesh is loaded correctly
        if not self.mesh.is_empty():
            print("STL file loaded successfully!")
        else:
            print("Failed to load STL file.")

    def visualize(self):
        # Compute vertex normals for better visualization
        self.mesh.compute_vertex_normals()

        # Visualize the 3D mesh
        o3d.visualization.draw_geometries([self.mesh])

    def to_point_cloud(self):
        point_cloud = self.mesh.sample_points_uniformly(number_of_points=10000)  # Adjust the number of points as needed






duck_file = os.path.abspath("../../docs/Rubber_Duck.stl")


duck = Object(duck_file, [0,0,500], [0,0,0])
pc = duck.to_point_cloud()

print(type(pc))

Lcam = Camera(2560,960, 2.43, [-50,0,0], [0,0,0])
Rcam = Camera(2560,960, 2.43, [50,0,0], [0,0,0])

#duck.visualize()

if __name__ == "__main__":
    pass