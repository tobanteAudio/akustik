import numpy as np


def rt60_target(volume) -> float:
    """Formula given in section 2.3 of 'EBU Tech. 3276'
    """
    T60_min = 0.2
    T60_max = 0.4
    V0 = 100
    return max(T60_min, min(T60_max, 0.25*(volume/V0)**(1/3)))
