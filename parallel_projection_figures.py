from math import sin, cos, sqrt, pi, floor
import numpy as np
import tkinter as tk

DISPLAY_HEIGHT_TO_WIDTH = 1.85;

viewer = np.array([0, 1, 0])
illumination = np.array([-11.99, -11.99, 0]) / sqrt(2)

illumnation_characters = ".,-~:;=!*#$@"

def get_character(phi):
    """
    Returns the ascii character to use for displaying the view
    when a plane is rotated with the given angle about the z-axis.
    It used the illumnation vector set in this file
    """
    # The normal vector to the surface
    normal = np.array([cos(phi), sin(phi), 0])
    # If the disc is facing the other way, return the reflection from 
    # the hind side instead
    if (normal[1] < 0):
        alternate_angle = phi + pi
        alternate_angle = alternate_angle if alternate_angle < 2*pi else alternate_angle - 2*pi
        return get_character(alternate_angle)
    # cv1 is the normal component of the light, and cv2 is parallel to the surface
    cv1 = np.sum(illumination * normal) * normal
    cv2 = illumination - cv1
    reflection = cv2 - cv1
    # Add the absolute value so that both sides of the disc reflect the same.
    viewer_component = (12 + np.sum(viewer * reflection)) / 2
    return illumnation_characters[floor(viewer_component)]

def get_circle_display(radius, phi):
    """
    Get a snapshot of a circle rotated at angle phi about the vertical axis
    """
    diameter = radius << 1
    character = get_character(round(phi, 6))
    horizontal_radius = int(round(radius * DISPLAY_HEIGHT_TO_WIDTH))
    rad_with_buffer = horizontal_radius * 1.1
    strings_list = []
    rad_squared = radius ** 2
    multiplier = sin(phi) * DISPLAY_HEIGHT_TO_WIDTH
    for i in range(0, diameter+1):
        height = radius - i
        perspective_radius = int(round(abs(sqrt(rad_squared - height**2) * multiplier)))
        leading_space = int(round(rad_with_buffer - perspective_radius))
        # leading space is equal to trailing space.
        final_string = (" "*leading_space) + (character * (perspective_radius * 2)) \
            + (" " * leading_space)
        strings_list.append(final_string)
    return strings_list


def get_diamond_display (half_diagonal, phi):
    """
    Get a snapshot of a diamond shape rotated at angle phi about the vertical axis,
    return as a list of ascii characters
    """
    diagonal = half_diagonal << 1
    character = get_character(round(phi, 6))
    horizontal_half_diagonal = half_diagonal * DISPLAY_HEIGHT_TO_WIDTH
    # Add some buffer for printing.
    full_half_width = horizontal_half_diagonal * 1.1
    multiplier = abs(horizontal_half_diagonal * sin(phi))
    strings_list = []
    for i in range(0, diagonal+1):
        unscaled_radius = i if i <= half_diagonal else diagonal - i
        scaled_radius = int(round(multiplier * unscaled_radius/half_diagonal))
        leading_space = int(round(full_half_width - scaled_radius))
        final_string = (" " * leading_space) + (character * (scaled_radius << 1)) \
            + (" " * leading_space)
        strings_list.append(final_string)
    return strings_list


display_library = dict()
def get_displays(radius, phase):
    rounded_phase = round(phase, 6)
    if not display_library.get(rounded_phase):
        circle_display = get_circle_display(radius, phase)
        # Add a 90 degree phase shift to the diamond. Looks a bit dope
        diamond_display = get_diamond_display(radius, phase+pi/2)
        joint_displays = []
        for i in range(len(circle_display)):
            joint_displays.append(circle_display[i] + diamond_display[i])
        final_string = "\n".join(joint_displays)
        display_library[rounded_phase] = final_string
    return display_library.get(rounded_phase)
#

delta_phi = pi/90
radius = 12
interval = 100

display_params = {
    "current_phase": 0,
    "string_to_display": get_displays(radius, 0)
}

def main():
    root = tk.Tk()
    root.configure(bg="black")
    label = tk.Label(root, text=display_params["string_to_display"], bg="black", fg="white", font=("Courier", 9))
    label.pack()

    def change_text():
        new_angle = display_params["current_phase"] + delta_phi
        display_params["current_phase"] = new_angle if new_angle < (2*pi) else new_angle - (2*pi)
        string_to_display = get_displays(radius, display_params["current_phase"])
        label["text"] = string_to_display
        root.after(interval, change_text)

    root.after(interval, change_text)
    root.mainloop()

if __name__ == "__main__":
    main()
