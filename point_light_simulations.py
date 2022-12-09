from math import sin, cos, sqrt, pi, floor
import numpy as np
import tkinter as tk

DISPLAY_HEIGHT_TO_WIDTH = 1.85;

viewer = np.array([0, 10, 0])
illumination = np.array([-11.99, -11.99, 0]) / sqrt(2)

illumnation_characters = ".,-~:;=!*#$@"

def get_character(point: np.ndarray, normal_vector: np.ndarray, light_source: np.ndarray = illumination):
    """
    Returns the ascii character to use for displaying a region after
    computing the reflection magnitude from the point
    """
    if np.sum(viewer * normal_vector) <= 0:
        return None
    light_vector: np.ndarray = point - light_source
    dot_product = np.sum(normal_vector * light_vector)
    orthogonal_part: np.ndarray = dot_product * normal_vector
    parallel_part: np.ndarray = light_vector - orthogonal_part

    # Get the reflection vector
    reflection = parallel_part - orthogonal_part

    # Direction toward viewer
    view_vector = viewer - point
    view_vector = view_vector / np.linalg.norm(view_vector)

    # Get the dot product of the reflected light intensity and the view vector
    reflection_toward_viewer = np.sum(reflection * view_vector)
    perceived_reflection = (reflection_toward_viewer + 12) /2
    return illumnation_characters[floor(perceived_reflection)]

