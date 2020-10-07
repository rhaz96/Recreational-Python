"""Build 2D model of barred-shaped galaxy using Ringermacher & Mead's equation."""
import numpy as np
import math
from random import randint, uniform, random
import tkinter as tk

root = tk.Tk()
root.title("Barred Spiral Galaxy")
c = tk.Canvas(root, width=1000, height=800, bg="black")
c.grid()
c.configure(scrollregion=(-500, -400, 500, 400))


def random_polar_coordinates(disc_radius_scaled):
    """Generate uniform random x,y point within a disc for 2-D display."""
    ##1##
    r = random()
    ##2##
    theta = uniform(0, 2 * math.pi)
    ##3##
    x = round(math.sqrt(r) * math.cos(theta) * disc_radius_scaled)
    y = round(math.sqrt(r) * math.sin(theta) * disc_radius_scaled)
    return x, y


def spirals(A, B, N, rot_fac, fuz_fac, arm):
    """Generate spiral arms for galaxy that follow the barred-galaxy equation of Ringermacher & Mead.
    
    A = scale/zoom parameter
    B = paramater to control the middle "bulge" or "bar" of the galaxy core
    N = paramter to control how tightly wound the spiral arms are
    rot_fac = angle at which to rotate a spiral arm
    fuzz_fac = parameter to add noise that spiral coordinates
    arm = whether spiral arm is leading (arm=1) or trailing (arm=0)
    """

    ##1##
    spiral_stars = []
    thetas = np.radians(np.arange(0.01, 90, 0.05))
    fuzz = 0.030 * abs(A)

    ##2##
    for theta in thetas:
        try:
            denom = B * math.tan(theta / (2 * N))
            x = (
                A / math.log(denom) * math.cos(theta + math.pi * rot_fac)
                + uniform(-fuzz, fuzz) * fuz_fac
            )
            y = (
                A / math.log(denom) * math.sin(theta + math.pi * rot_fac)
                + uniform(-fuzz, fuzz) * fuz_fac
            )
            spiral_stars.append((x, y))
        except ValueError:
            print(denom)
            print("Cannot take the natural log of 0 or a negative number.  Try again.")

    ##3##
    for x, y in spiral_stars:
        if arm == 0 and math.ceil(x) % 2 == 0:
            c.create_oval(x - 1, y - 1, x + 1, y + 1, fill="#33D4FF", outline="")
        elif arm == 0 and math.ceil(x) % 2 != 0:
            c.create_oval(x - 1, y - 1, x + 1, y + 1, fill="white", outline="")
        elif arm == 1:
            c.create_oval(x, y, x, y, fill="white", outline="")
    return spiral_stars


def ellipse(x, y, theta, a, b):
    """ Polar coordinate form of an ellipse to design galaxy core.
    
    x = x input
    y = y input
    theta = angle of rotation of ellipse
    a = squared radius of major axis
    b = squared radius of minor axis
    """

    ##1##
    axis_1 = (x * math.cos(theta) - y * math.sin(theta)) ** 2 / a
    axis_2 = (x * math.sin(theta) - y * math.cos(theta)) ** 2 / b
    return axis_1 + axis_2


def star_haze(disc_radius_scaled, density):
    """Randomly distribute faint tkinter stars in galactic disc.
    
    disc_radius_scaled = radius of galaxy disc.  Larger values will obscure the edges
    density = multiplier to vary number of stars posted
    """

    ##1##
    haze_coords = [
        random_polar_coordinates(disc_radius_scaled)
        for _ in range(disc_radius_scaled * density)
    ]
    ##2##
    for x, y in haze_coords:
        ellipse_haze = ellipse(x, y, -8, 4, 6)
        if np.isclose(ellipse_haze, 300, 10):
            c.create_oval(
                x - 1.5, y - 1.5, x + 1.5, y + 1.5, fill="#F0D3CD", outline=""
            )
        elif x % 2 == 0 and y % 2 == 0:
            c.create_oval(x, y, x, y, fill="red", outline="")
        else:
            c.create_oval(x, y, x, y, fill="white", outline="")


def main():
    """ Create the spirals and elliptic core."""
    # clockwise spirals
    spirals(A=650, B=10, N=50, rot_fac=0, fuz_fac=3, arm=0)
    spirals(A=650, B=10, N=50, rot_fac=0.07, fuz_fac=1, arm=1)
    spirals(A=650, B=10, N=50, rot_fac=0.20, fuz_fac=1, arm=1)
    spirals(A=650, B=10, N=50, rot_fac=0.30, fuz_fac=2, arm=1)
    # counterclockwise spirals
    spirals(A=-650, B=10, N=50, rot_fac=0, fuz_fac=3, arm=0)
    spirals(A=-650, B=10, N=50, rot_fac=0.07, fuz_fac=1, arm=1)
    spirals(A=-650, B=10, N=50, rot_fac=0.20, fuz_fac=1, arm=1)
    spirals(A=-650, B=10, N=50, rot_fac=0.30, fuz_fac=2, arm=1)
    # elliptic core
    star_haze(700, 40)
    # don't turn off tk screen unless user clicks close
    root.mainloop()


if __name__ == "__main__":
    main()