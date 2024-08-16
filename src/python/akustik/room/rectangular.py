import numpy as np
import sympy as sp


def room_mode(L, W, H, m, n, p, c=343):
    return c*0.5*np.sqrt((m/L)**2 + (n/W)**2 + (p/H)**2)


def room_mode_kind(m, n, p):
    non_zero = (m != 0) + (n != 0) + (p != 0)
    if non_zero == 1:
        return "axial"
    if non_zero == 2:
        return "tangential"
    return "oblique"


def frequency_spacing_index(L, W, H):
    modes = []
    max_order = 6
    for m in range(max_order+1):
        for n in range(max_order+1):
            for p in range(max_order+1):
                if m+n+p > 0:
                    modes.append({
                        "m": m,
                        "n": n,
                        "p": p,
                        "frequency": room_mode(L, W, H, m, n, p)
                    })

    modes = sorted(modes, key=lambda x: x['frequency'])[:25]

    psi = 0.0
    num = len(modes)
    f0 = modes[0]['frequency']
    fn = modes[-1]['frequency']
    delta_hat = (fn-f0)/(num-1)
    for n in range(1, num):
        prev = modes[n-1]['frequency']
        freq = modes[n]['frequency']
        delta = freq-prev
        psi += (delta/delta_hat)**2

    fsi = psi / (num-1)
    return fsi


def preferred_dimensions(L=None, W=None, H=None, A=None, ratio="A"):
    """Preferred dimension ratios of small rectangular rooms
    """
    ratios = {
        "A": {"w/h": 1.2, "l/h": 1.45, "l/w": 1.21},
        "B": {"w/h": 1.4, "l/h": 1.89, "l/w": 1.35},
    }
    assert ratio in "AB"
    assert L or A
    assert not (W or H)

    wh = ratios[ratio]["w/h"]
    lh = ratios[ratio]["l/h"]
    lw = ratios[ratio]["l/w"]

    l = sp.Symbol('L', positive=True)
    w = sp.Symbol('W', positive=True)
    h = sp.Symbol('H', positive=True)

    if L:
        result = sp.solve([l-L, l/h-lh, l/w-lw], [l, w, h], dict=True)
        L = result[0][l]
        W = result[0][w]
        H = result[0][h]

    if A:
        system = [w/h-wh, l/h-lh, l/w-lw, l*w-A]
        result = sp.solve(system, [l, w, h], dict=True)
        L = result[0][l]
        W = result[0][w]
        H = result[0][h]

    return np.array([L, W, H])
