import numpy as np


def surface_area_cyclinder(r, h, with_bottom=True, with_top=True):
    area = 2*np.pi*r*h
    if with_bottom:
        area += 2*np.pi*r**2
    if with_top:
        area += 2*np.pi*r**2
    return area


def volume_cyclinder(r, h):
    V = np.pi*r**2*h
    return V


def volume_hollow_cyclinder(R, r, h):
    V = np.pi*(R**2-r**2)*h
    return V


def main():
    # Inner Diameter, Insulation Thickness, Price per 1m
    tubes = [
        (0.219, 0.05, 40.62),
        (0.219, 0.06, 47.25),
        (0.219, 0.07, 54.49),
        (0.219, 0.10, 77.30),
        (0.219, 0.12, 94.50),
        (0.273, 0.05, 60.05),
    ]

    for tube in tubes:
        h = 1.0
        inner_radius = tube[0]/2
        outer_radius = inner_radius+tube[1]
        area = surface_area_cyclinder(outer_radius, h, False, False)
        volume = volume_cyclinder(outer_radius, h)*1000
        damping = volume_hollow_cyclinder(outer_radius, inner_radius, h)*1000
        euro_per_volume = tube[2]/damping
        print(f"----- {tube[0]*1000:.0f} / {tube[1]*1000:.0f} -----")
        print(f"diameter      = {outer_radius*2:.2f} m")
        print(f"circumference = {outer_radius*2*np.pi:.2f} m")
        print(f"area          = {area:.2f} m^2")
        print(f"volume        = {volume:.2f} litre")
        print(f"damping       = {damping:.2f} litre")
        print(f"price         = {tube[2]:.2f} Euro")
        print(f"cost          = {euro_per_volume:.2f} Euro / litre")
        print("")
