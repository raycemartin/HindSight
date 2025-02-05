import numpy as np
import cv2
import matplotlib.pyplot as plt

class Image:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.img = np.zeros(self.width, self.height)
