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

display_library = dict()
def get_display(radius, phi):
    rounded_value = round(phi, 6)
    if not display_library.get(rounded_value):
        strings_list = []
        diameter = radius << 1
        character = get_character(rounded_value)
        horizontal_radius = radius * DISPLAY_HEIGHT_TO_WIDTH
        for i in range(0, diameter+1):
            height = max(radius-i, i-radius)
            perspective_radius = abs(int(sqrt(radius ** 2 - height**2) * sin(phi) * DISPLAY_HEIGHT_TO_WIDTH))
            leading_space = max(int(round(horizontal_radius)) - perspective_radius, 0)
            # leading space is equal to trailing space.
            final_string = (" "*leading_space) + (character * (perspective_radius * 2) \
                + " " * leading_space)
            strings_list.append(final_string)
        display_library[rounded_value] = "\n".join(strings_list)
    return display_library.get(rounded_value)


# def main():

delta_phi = pi/180
radius = 17
interval = 80

display_params = {
    "current_angle": 0,
    "string_to_display": get_display(radius, 0)
}

def main():
    root = tk.Tk()
    root.configure(bg="black")
    label = tk.Label(root, text=display_params["string_to_display"], bg="black", fg="white", font="Courier")
    label.pack()

    def change_text():
        new_angle = display_params["current_angle"] + delta_phi
        display_params["current_angle"] = new_angle if new_angle < (2*pi) else new_angle - (2*pi)
        string_to_display = get_display(radius, display_params["current_angle"])
        label["text"] = string_to_display
        root.after(interval, change_text)

    root.after(interval, change_text)
    root.mainloop()

if __name__ == "__main__":
    main()
