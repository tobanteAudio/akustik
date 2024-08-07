import numpy as np


def mode(L, W, H, m, n, p):
    c = 343
    return c*0.5*np.sqrt((m/L)**2 + (n/W)**2 + (p/H)**2)


def mode_kind(m, n, p):
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
                        "frequency": mode(L, W, H, m, n, p)
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
