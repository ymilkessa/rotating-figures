from math import sin, cos, sqrt, pi, floor
import numpy as np
import tkinter as tk

DISPLAY_HEIGHT_TO_WIDTH = 1.85;

# viewer = np.array([0, 100, 0])
viewer = np.array([0,30,0])
# light_source_location = np.array([70.71, 70.71, 0])
light_source_location = np.array([18, 18, 0])

# TODO: the light intensity should also very by distance
max_illumination = 12

illumnation_characters = ".,-~:;=!*#$@"

def get_reflection(point: np.ndarray, normal_vector: np.ndarray, light_source: np.ndarray = light_source_location):
    """
    Returns the ascii character to use for displaying a region after
    computing the reflection magnitude from the point
    """
    if np.sum(viewer * normal_vector) <= 0:
        return 0
    # Get the direction of incoming light and multiply by the right magnitude
    light_vector: np.ndarray = point - light_source
    light_vector = (light_vector / np.linalg.norm(light_vector)) * max_illumination
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
    return (reflection_toward_viewer + 12) /2

def get_rotation_matrix(phi: float):
    cos_phi = cos(phi)
    sin_phi = sin(phi)
    operator = np.array([
        [cos_phi, 0-sin_phi, 0],
        [sin_phi, cos_phi, 0],
        [0,0,1]
        ])
    return operator

def get_circle_display(radius, phi):
    """
    Get a snapshot of a disc rotated to angle phi about the vertical,
    and where both the light source and the viewer are points in space.
    """
    strings_list = []

    # Get the rotating operator and the current normal vector to the disc
    operator = get_rotation_matrix(phi)
    current_normal = np.matmul(operator, np.array([1,0,0]))
    if np.sum(viewer * current_normal) < 0:
        alternate_angle = phi + pi
        alternate_angle = alternate_angle if alternate_angle < 2*pi else alternate_angle - 2*pi
        return get_circle_display(radius, alternate_angle)

    # These are computed out here since they keep getting reused.
    rad_squared = radius ** 2
    multiplier = sin(phi) * DISPLAY_HEIGHT_TO_WIDTH
    horizontal_radius = int(round(radius * DISPLAY_HEIGHT_TO_WIDTH))
    rad_with_buffer = horizontal_radius * 1.1
    for i in range(0, (radius << 1)+1):
        height = radius - i
        # TODO: This perspective radius is an approximation. Should be changed to make the logic
        # accurate.
        perspective_radius = int(round(abs(sqrt(rad_squared - height**2) * multiplier)))

        # Start the final string with the leading space
        leading_space = int(round(rad_with_buffer - perspective_radius))
        final_string = " " * leading_space                     

        # Now loop through each spot and compute the character to use for it
        for k in range(perspective_radius << 1):
            coord_0 = perspective_radius - k
            current_position = np.matmul(operator, np.array([coord_0, 0, height]))
            reflection_magnitude = get_reflection(current_position, current_normal)
            
            # Add the character to the string to append
            final_string += illumnation_characters[floor(reflection_magnitude)]

        # Add a symmetric amount of white space for the "trailing space"
        final_string += " " * leading_space
        strings_list.append(final_string)
    return strings_list

display_library = dict()
def get_display(radius, phase):
    rounded_phase = round(phase, 6)
    if not display_library.get(rounded_phase):
        circle_display = get_circle_display(radius, phase)
        final_string = "\n".join(circle_display)
        display_library[rounded_phase] = final_string
    return display_library.get(rounded_phase)
#

delta_phi = pi/30
radius = 15
interval = 100

display_params = {
    "current_phase": 0,
    "string_to_display": get_display(radius, 0)
}

def main():
    root = tk.Tk()
    root.configure(bg="black")
    label = tk.Label(root, text=display_params["string_to_display"], bg="black", fg="white", font=("Courier", 9))
    label.pack()

    def change_text():
        new_angle = display_params["current_phase"] + delta_phi
        display_params["current_phase"] = new_angle if new_angle < (2*pi) else new_angle - (2*pi)
        string_to_display = get_display(radius, display_params["current_phase"])
        label["text"] = string_to_display
        root.after(interval, change_text)

    root.after(interval, change_text)
    root.mainloop()

if __name__ == "__main__":
    main()
