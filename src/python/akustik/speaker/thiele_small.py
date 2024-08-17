import numpy as np
import pandas as pd


def _estimate_f1_f2(fs, f1=None, f2=None):
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


def main(driver_db, drivers):
    for name in drivers:
        df = pd.read_csv(driver_db)
        driver = df[df['Name'] == name]
        Cms = float(driver["Cms"].iloc[0])
        fs = float(driver["fs"].iloc[0])
        f1 = float(driver["f1"].iloc[0])
        f2 = float(driver["f2"].iloc[0])
        n0 = float(driver["n0"].iloc[0])
        Qes = float(driver["Qes"].iloc[0])
        Qms = float(driver["Qms"].iloc[0])
        Qts = float(driver["Qts"].iloc[0])
        Re = float(driver["Re"].iloc[0])
        Sd = float(driver["Sd"].iloc[0])
        Zmax = float(driver["Zmax"].iloc[0])
        Vas = float(driver["Vas"].iloc[0])/1000

        # Zmax = 51
        # f1, f2 = _estimate_f1_f2(fs, f2=450)

        fs_prime = np.sqrt(f1*f2)
        R0 = Zmax / Re
        Z12 = np.sqrt(Re*Zmax)
        Qms_prime = mechanical_q_factor(fs, f1, f2, R0)
        Qes_prime = electrical_q_factor(Qms_prime, R0)
        Qts_prime = total_q_factor(Qms_prime, Qes_prime)
        Mms = effective_moving_mass(fs, Cms)
        Vas = compliance_equivalent_volume(Sd, Cms)
        n0_prime = efficiency(fs, Qes_prime, Vas)
        SPL_prime = 112.02 + 10*np.log10(n0_prime) + 10*np.log10(8/Re)

        print(name)
        print(f"{fs=:.2f} Hz")
        print(f"{f1=:.2f} Hz")
        print(f"{f2=:.2f} Hz")
        print(f"{Mms=:.4f} kg")
        print(f"{n0=:.4f}")
        print(f"{Qes=:.4f}")
        print(f"{Qms=:.4f}")
        print(f"{Qts=:.4f}")
        print(f"{R0=:.4f}")
        print(f"{Re=:.4f}")
        print(f"{Vas=:.4f} m^3")
        print(f"{Z12=:.4f} Ohm")
        print(f"{Zmax=:.4f} Ohm")
        print("")

        print(f"{fs_prime=:.2f} Hz")
        print(f"{n0_prime=:.4f}")
        print(f"{SPL_prime=:.4f} dB")
        print(f"{Qms_prime=:.4f}")
        print(f"{Qes_prime=:.4f}")
        print(f"{Qts_prime=:.4f}")
        print("")

        print(f"{fs-fs_prime=:.2f} Hz")
        print(f"{n0-n0_prime=:.4f}")
        print(f"{Qms-Qms_prime=:.4f}")
        print(f"{Qes-Qes_prime=:.4f}")
        print(f"{Qts-Qts_prime=:.4f}")

    # print("")
    # print(f"{resonance_frequency(Cms=0.0003, Mms=0.5)=:.2f}Hz")
    # print(f"{resonance_frequency(Cms=0.0003, Mms=0.6)=:.2f}Hz")
    # print(f"{resonance_frequency(Cms=0.0003, Mms=0.7)=:.2f}Hz")

    # print("")
    # print(f"{resonance_frequency(Cms=0.00025, Mms=0.5)=:.2f}Hz")
    # print(f"{resonance_frequency(Cms=0.00025, Mms=0.6)=:.2f}Hz")
    # print(f"{resonance_frequency(Cms=0.00025, Mms=0.7)=:.2f}Hz")
