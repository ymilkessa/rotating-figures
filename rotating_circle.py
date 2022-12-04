from math import sin, sqrt, pi
import tkinter as tk

DISPLAY_HEIGHT_TO_WIDTH = 1.85;

def getCharacter(phi):
    return "#"
    # if phi == pi/2:
    #     return "#"
    # elif phi == 0:
    #     return "|"
    # else:
    #     return "/"

def get_display(radius, phi):
    strings_list = []
    diameter = radius << 1
    character = "#" # getCharacter(phi)
    horizontal_radius = radius * DISPLAY_HEIGHT_TO_WIDTH
    for i in range(0, diameter+1):
        height = max(radius-i, i-radius)
        perspective_radius = abs(int(sqrt(radius ** 2 - height**2) * sin(phi) * DISPLAY_HEIGHT_TO_WIDTH))
        leading_space = max(int(round(horizontal_radius)) - perspective_radius, 0)
        # leading space is equal to trailing space.
        final_string = (" "*leading_space) + (character * (perspective_radius * 2) \
            + " " * leading_space)
        strings_list.append(final_string)
    # print("\n".join(strings_list))
    final_string = "\n".join(strings_list)
    return final_string


# def main():

delta_phi = pi/180
radius = 17
interval = 100

display_params = {
    "current_angle": 0,
    "string_to_display": get_display(radius, 0)
}

root = tk.Tk()
root.configure(bg="black")
# current_angle = 0
# string_to_display = get_display(radius, current_angle)
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

# class RotatingCircle:
#     def __init__(self) -> None:
#         self.root = tk.Tk()
#         self.root.configure(bg="black")
#         self.current_angle = 0
#         self.delta_phi = pi/180
#         self.radius = 17
#         self.string_to_display = "Hi"
#         self.label = None
#         self.initial_display()

#     def initial_display(self):
#         self.string_to_display = get_display(self.radius, self.current_angle)
#         self.label = tk.Label(self.root, text=self.string_to_display, bg="black", fg="white", font="Courier")

#     def rotate_circle(self):
#         new_angle = self.current_angle + self.delta_phi
#         self.current_angle = new_angle if new_angle < (2*pi) else (2*pi) - new_angle
#         self.string_to_display = get_display(self.radius, self.current_angle)
#         if (self.label):
#             self.label["text"] = self.string_to_display
#         self.root.after(500, self.rotate_circle) 
#         self.root.mainloop()  


# if __name__=="__main__":
#     RotatingCircle().rotate_circle()
