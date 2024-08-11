import numpy as np


def _find_f1_f2(fs, f1=None, f2=None):
    assert f1 or f2

    if f1:
        f2 = fs**2 / f1
    else:
        f1 = fs**2 / f2

    return f1, f2


def compliance_equivalent_volume(Sd, Cms, rho=1.2, c=343):
    Vas = Cms * rho * c**2 * Sd**2
    return Vas


def effective_moving_mass(fs, Cms):
    Mms = 1 / ((2 * np.pi * fs)**2 * Cms)
    return Mms


def efficiency(fs, Qes, Vas, c=343):
    n0 = (4.0 * np.pi**2 * fs**3 * Vas) / (c**3 * Qes)
    return n0


def electrical_q_factor(Qms, R0):
    Qes = Qms/(R0-1)
    return Qes


def mechanical_q_factor(fs, f1, f2, R0):
    Qms = fs/(f2-f1)*np.sqrt(R0)
    return Qms


def resonance_frequency(Cms, Mms):
    fs = 1.0/(2*np.pi*np.sqrt(Cms*Mms))
    return fs


def total_q_factor(Qms, Qes):
    Qts = (Qms * Qes) / (Qms + Qes)
    return Qts


def report():
    # # Volt Loudspeakers RV3143
    # Re = 6.1
    # fs = 35.0
    # Qms = 5.35
    # Qes = 0.32
    # Sd = 0.0473
    # Cms = 0.00027
    # Zmax = 95
    # f1, f2 = _find_f1_f2(fs, f2=50.5)

    # # Dayton Audio RSS315HF-4
    # Re = 3.1
    # fs = 24.2
    # n0 = 0.254
    # Qms = 2.83
    # Qes = 0.449
    # Sd = 0.05147
    # Cms = 0.00023
    # Zmax = 22.438
    # f1, f2 = _find_f1_f2(fs, f2=38.05)

    # Dayton Audio RSS315HFA-8
    Re = 6.52
    fs = 21.983
    n0 = 0.188
    Qms = 2.5
    Qes = 0.541
    Sd = 0.05147
    Cms = 0.00027
    Zmax = 36.328
    f1, f2 = 13.85, 34.896

    # Supravox 400 GMF
    # Re = 6.5
    # fs = 18.87
    # n0 = 0.0
    # Qms = 7.5492
    # Qes = 0.1432
    # Sd = 0.0855
    # Cms = 0.00027
    # Zmax = 350
    # f1, f2 = _find_f1_f2(fs, f2=30.1)

    fs_prime = np.sqrt(f1*f2)
    R0 = Zmax / Re
    Z12 = np.sqrt(Re*Zmax)
    Qts = total_q_factor(Qms, Qes)
    Qms_prime = mechanical_q_factor(fs, f1, f2, R0)
    Qes_prime = electrical_q_factor(Qms_prime, R0)
    Qts_prime = total_q_factor(Qms_prime, Qes_prime)
    Mms = effective_moving_mass(fs, Cms)
    Vas = compliance_equivalent_volume(Sd, Cms)
    n0_prime = efficiency(fs, Qes_prime, 0.0972)*100

    Mms *= 1000
    Vas *= 1000

    # print(f"{resonance_frequency(Cms, Mms)=:.2f} Hz")
    print(f"{fs=:.2f} Hz")
    print(f"{f1=:.2f} Hz")
    print(f"{f2=:.2f} Hz")
    print(f"{Mms=:.4f} g")
    print(f"{n0=:.4f}")
    print(f"{Qes=:.4f}")
    print(f"{Qms=:.4f}")
    print(f"{Qts=:.4f}")
    print(f"{R0=:.4f}")
    print(f"{Vas=:.4f} litre")
    print(f"{Z12=:.4f} Ohm")
    print(f"{Zmax=:.4f} Ohm")
    print("")

    print(f"{fs_prime=:.2f} Hz")
    print(f"{n0_prime=:.4f}")
    print(f"{Qms_prime=:.4f}")
    print(f"{Qes_prime=:.4f}")
    print(f"{Qts_prime=:.4f}")
    print("")

    print(f"{fs-fs_prime=:.2f} Hz")
    print(f"{n0-n0_prime=:.4f}")
    print(f"{Qms-Qms_prime=:.4f}")
    print(f"{Qes-Qes_prime=:.4f}")
    print(f"{Qts-Qts_prime=:.4f}")


report()
