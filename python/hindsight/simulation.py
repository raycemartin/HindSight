import numpy as np
import cv2
import matplotlib.pyplot as plt
import open3d as o3d
import os

class Camera:
    def __init__(self, width, height, f, coordinate: list, orientation: list):
        self.width = width
        self.height = height
        self.f = f
        self.coordinate = coordinate
        self.orientation = orientation

        self.img = np.zeros(self.width, self.height)

class Object:
    def __init__(self,filename: str):
        if not isinstance(filename, str):
            raise TypeError("The filename must be a string.")

        self.mesh = o3d.io.read_triangle_mesh(filename)

duck_file = os.path.abspath("../../docs/Rubber_Duck.stl")


duck = Object(duck_file)

if __name__ == "__main__":
    pass